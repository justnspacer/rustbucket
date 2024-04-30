namespace RustyTech.Server.Models
{
    public class Response<T>
    {
        public int StatusCode { get; set; }
        public string Message { get; set; }
        public T Data { get; set; }

        public Response(int statusCode, string message, T data)
        {
            StatusCode = statusCode;
            Message = message;
            Data = data;
        }

        public static Response<T> Success(T data, string message = "")
        {
            return new Response<T>(200, message, data);
        }

        public static Response<T> Error(int statusCode, string message)
        {
            return new Response<T>(statusCode, message, default(T));
        }
    }
}
