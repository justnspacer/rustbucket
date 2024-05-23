using Newtonsoft.Json;

namespace RustyTech.Server.Models
{
    public class ApiResponse<T>
    {
        [JsonProperty("status_code")]
        public int StatusCode { get; set; }

        [JsonProperty("message")]
        public string? Message { get; set; }

        [JsonProperty("data")]
        public T? Data { get; set; }

        public ApiResponse(int statusCode, string? message, T? data)
        {
            StatusCode = statusCode;
            Message = message;
            Data = data;
        }

        public static ApiResponse<T> Success(string message, T data)
        {
            return new ApiResponse<T>(200, message, data);
        }

        public static ApiResponse<T> Error(int statusCode, string message)
        {
            return new ApiResponse<T>(statusCode, message, default(T));
        }
    }
}
