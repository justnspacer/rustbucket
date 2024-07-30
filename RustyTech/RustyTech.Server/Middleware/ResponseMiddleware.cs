using Newtonsoft.Json;
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
            try
            {
                Stream originalBodyStream = context.Response.Body;
                using (var newBodyStream = new MemoryStream())
                {
                    context.Response.Body = newBodyStream;

                    await _next(context);

                    context.Response.Body.Seek(0, SeekOrigin.Begin);
                    string readBuffer = await new StreamReader(context.Response.Body).ReadToEndAsync();

                    context.Response.Body = originalBodyStream;

                    ApiResponse<object> response = new ApiResponse<object>(JsonConvert.DeserializeObject(readBuffer));
                    await WriteResponse(response, context);
                }
            }
            catch (Exception ex)
            {
                ApiResponse<object> response = new ApiResponse<object>(ex.Message);
                await WriteResponse(response, context);
            }
        }

        private async Task WriteResponse(ApiResponse<object> response, HttpContext context)
        {
            var responseJson = JsonConvert.SerializeObject(response);
            var responseBytes = Encoding.UTF8.GetBytes(responseJson);
            context.Response.ContentType = "application/json";
            await context.Response.Body.WriteAsync(responseBytes, 0, responseBytes.Length);
        }
    }
}
