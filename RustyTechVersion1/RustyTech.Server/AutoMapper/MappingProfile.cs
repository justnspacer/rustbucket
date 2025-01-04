using AutoMapper;
using RustyTech.Server.Models.Dtos;
using RustyTech.Server.Models.Posts;

namespace RustyTech.Server.AutoMapper
{
    public class MappingProfile : Profile
    {
        public MappingProfile()
        {
            CreateMap<User, GetUserRequest>();

            CreateMap<BlogPost, CreateBlogRequest>().ForMember(destination => destination.User, option => option.MapFrom(source => source.User));
            CreateMap<ImagePost, CreateImageRequest>().ForMember(destination => destination.User, option => option.MapFrom(source => source.User));
            CreateMap<VideoPost, CreateVideoRequest>().ForMember(destination => destination.User, option => option.MapFrom(source => source.User));

            CreateMap<BlogPost, GetPostRequest>().ForMember(destination => destination.User, option => option.MapFrom(source => source.User));

            CreateMap<ImagePost, GetPostRequest>().ForMember(destination => destination.User, option => option.MapFrom(source => source.User));

            CreateMap<VideoPost, GetPostRequest>().ForMember(destination => destination.User, option => option.MapFrom(source => source.User));

        }
    }
}
