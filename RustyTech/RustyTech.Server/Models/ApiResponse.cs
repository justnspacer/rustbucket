namespace RustyTech.Server.Models
{
    public class ApiResponse<T>
    {
        public int StatusCode { get; set; }
        
        public T Data { get; set; }

        public ApiResponse(int statusCode, T data)
        {
            StatusCode = statusCode;
            Data = data;
        }

        public static ApiResponse<T> Success(T data)
        {
            return new ApiResponse<T>(200, data);
        }

        public static ApiResponse<T> Error(int statusCode)
        {
            return new ApiResponse<T>(statusCode, default(T));
        }
    }
}
