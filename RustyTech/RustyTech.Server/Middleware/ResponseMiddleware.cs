using Newtonsoft.Json;
using RustyTech.Server.Models;
using System.Text;

namespace RustyTech.Server.Middleware
{
    public class ResponseMiddleware
    {
        private readonly RequestDelegate _next;

        public ResponseMiddleware(RequestDelegate next)
        {
            _next = next;
        }

        public async Task InvokeAsync(HttpContext context)
        {
            var originalBodyStream = context.Response.Body;
            using (var newBodyStream = new MemoryStream())
            {
                context.Response.Body = newBodyStream;

                await _next(context);

                context.Response.Body.Seek(0, SeekOrigin.Begin);
                var readBuffer = new StreamReader(context.Response.Body).ReadToEnd();

                var apiResponse = Response<object>.Success(JsonConvert.DeserializeObject(readBuffer));

                var responseToReturn = JsonConvert.SerializeObject(apiResponse);
                var responseBytes = Encoding.UTF8.GetBytes(responseToReturn);
                context.Response.Body = originalBodyStream;  // Reset the original stream
                context.Response.ContentType = "application/json";  // Set Content Type
                await context.Response.Body.WriteAsync(responseBytes, 0, responseBytes.Length);
            }
        }
    }
}
