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

            CreateMap<BlogPost, CreateBlogRequest>().ForMember(destionation => destionation.User, option => option.MapFrom(source => source.User));
            CreateMap<ImagePost, CreateImageRequest>().ForMember(destionation => destionation.User, option => option.MapFrom(source => source.User));
            CreateMap<VideoPost, CreateVideoRequest>().ForMember(destionation => destionation.User, option => option.MapFrom(source => source.User));

            CreateMap<BlogPost, GetPostRequest>().ForMember(destionation => destionation.User, option => option.MapFrom(source => source.User)).ForMember(destionation => destionation.ImageFile, option => option.Ignore());
            CreateMap<ImagePost, GetPostRequest>().ForMember(destionation => destionation.User, option => option.MapFrom(source => source.User));
            CreateMap<VideoPost, GetPostRequest>().ForMember(destionation => destionation.User, option => option.MapFrom(source => source.User));

        }
    }
}
