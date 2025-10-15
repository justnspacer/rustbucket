"""Flask application for receiving SMS webhooks."""

from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import asyncio
from command_processor import CommandProcessor
from security import Security
from config import MONITOR_CONFIG, SECURITY_CONFIG, FLASK_CONFIG, GATEKEEPER_CONFIG
from gatekeeper_client import GatekeeperClientManager, check_gatekeeper_health, get_available_services
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize command processor and security
command_processor = CommandProcessor(MONITOR_CONFIG)
security = Security(SECURITY_CONFIG)

# Initialize Gatekeeper client
gatekeeper_client = GatekeeperClientManager.initialize(GATEKEEPER_CONFIG)
logger.info(f"Initialized Gatekeeper client: {GATEKEEPER_CONFIG['gatekeeper_url']}")



@app.route('/sms', methods=['POST'])
def sms_webhook():
    """
    Handle incoming SMS webhook from Twilio.
    
    This endpoint receives SMS messages, verifies the sender,
    processes commands, and sends responses.
    """
    # Verify Twilio signature
    if not security.verify_twilio_signature(request):
        app.logger.warning(f"Invalid Twilio signature from {request.remote_addr}")
        return "Unauthorized", 401
    
    # Get message details
    from_number = request.form.get('From', '')
    message_body = request.form.get('Body', '')
    
    # Check authorization
    if not security.is_authorized(from_number):
        app.logger.warning(f"Unauthorized access attempt from {from_number}")
        response = MessagingResponse()
        response.message("❌ Unauthorized. Your number is not registered.")
        return str(response)
    
    # Log the incoming message
    app.logger.info(f"Received SMS from {from_number}: {message_body}")
    
    # Process the command asynchronously
    try:
        # Run async command processor in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response_text = loop.run_until_complete(command_processor.process(message_body))
        loop.close()
    except Exception as e:
        app.logger.error(f"Error processing command: {str(e)}", exc_info=True)
        response_text = f"❌ Error processing command: {str(e)}"
    
    # Send response via TwiML
    response = MessagingResponse()
    response.message(response_text)
    
    app.logger.info(f"Sending response to {from_number}: {response_text[:100]}")
    
    return str(response)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return {
        'status': 'healthy',
        'service': 'operator'
    }, 200


@app.route('/', methods=['GET'])
def index():
    """Index page with service information."""
    return {
        'service': 'Operator',
        'description': 'Command Processing Service for SMS',
        'endpoints': {
            '/sms': 'SMS webhook (POST)',
            '/health': 'Health check (GET)',
            '/gateway': 'Gateway information (GET)',
            '/gateway/health': 'Check gateway health (GET)',
            '/gateway/services': 'List gateway services (GET)',
        }
    }, 200


@app.route('/gateway', methods=['GET'])
def gateway_info():
    """Get information about the gatekeeper gateway connection."""
    return {
        'gateway_url': GATEKEEPER_CONFIG['gatekeeper_url'],
        'service_name': GATEKEEPER_CONFIG['service_name'],
        'timeout': GATEKEEPER_CONFIG['gatekeeper_timeout'],
        'status': 'configured'
    }, 200


@app.route('/gateway/health', methods=['GET'])
def gateway_health():
    """Check the health of the gatekeeper gateway."""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(check_gatekeeper_health(GATEKEEPER_CONFIG))
        loop.close()
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error checking gateway health: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to check gateway health: {str(e)}'
        }), 500


@app.route('/gateway/services', methods=['GET'])
def gateway_services():
    """Get list of available services from the gateway."""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(get_available_services(GATEKEEPER_CONFIG))
        loop.close()
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error getting gateway services: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to get gateway services: {str(e)}'
        }), 500


if __name__ == '__main__':
    # Run Flask app
    app.run(
        host=FLASK_CONFIG['host'],
        port=FLASK_CONFIG['port'],
        debug=FLASK_CONFIG['debug']
    )
