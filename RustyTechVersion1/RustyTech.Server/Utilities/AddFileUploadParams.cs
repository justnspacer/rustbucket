using Microsoft.OpenApi.Models;
using Swashbuckle.AspNetCore.SwaggerGen;

namespace RustyTech.Server.Utilities
{
    public class AddFileUploadParams : IOperationFilter
    {
        public void Apply(OpenApiOperation operation, OperationFilterContext context)
        {
            var fileParams = context.MethodInfo.GetParameters()
                .Where(p => p.ParameterType == typeof(IFormFile) || (p.ParameterType.IsGenericType && p.ParameterType.GetGenericTypeDefinition() == typeof(IEnumerable<>) && p.ParameterType.GetGenericArguments()[0] == typeof(IFormFile)));

            foreach (var param in fileParams)
            {
                var parameterToRemove = operation.Parameters.FirstOrDefault(p => p.Name == param.Name);
                if (parameterToRemove != null)
                {
                    operation.Parameters.Remove(parameterToRemove);
                }

                var schema = new OpenApiSchema
                {
                    Type = "object",
                    Properties = new Dictionary<string, OpenApiSchema>
                    {
                        [param.Name] = new OpenApiSchema
                        {
                            Type = param.ParameterType == typeof(IFormFile) ? "string" : "array",
                            Items = new OpenApiSchema { Type = "string", Format = "binary" },
                            Format = "binary"
                        }
                    }
                };

                operation.RequestBody = new OpenApiRequestBody
                {
                    Content =
                    {
                        ["multipart/form-data"] = new OpenApiMediaType
                        {
                            Schema = schema
                        }
                    }
                };
            }
        }
    }
}
