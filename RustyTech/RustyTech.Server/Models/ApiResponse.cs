using Newtonsoft.Json;

namespace RustyTech.Server.Models
{
    public class ApiResponse<T>
    {
        [JsonProperty("data")]
        public T? Data { get; set; }

        public ApiResponse(T? data)
        {
            Data = data;
        }

        public static ApiResponse<T> Success(T data)
        {
            return new ApiResponse<T>(data);
        }

        public static ApiResponse<T> Error()
        {
            return new ApiResponse<T>(default(T));
        }
    }
}
