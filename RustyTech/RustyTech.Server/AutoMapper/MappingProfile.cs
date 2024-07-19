using AutoMapper;

namespace RustyTech.Server.AutoMapper
{
    public class MappingProfile : Profile
    {
        public MappingProfile()
        {
            CreateMap<User, UserDto>();

            CreateMap<Post, PostDto>().ForMember(destionation => destionation.User, option => option.MapFrom(source => source.User));
            CreateMap<Post, PostDto>().ForMember(destionation => destionation.Keywords, option => option.MapFrom(source => source.Keywords));
            CreateMap<Blog, PostDto>().ForMember(destionation => destionation.ImageUrls, option => option.MapFrom(source => source.ImageUrls));
            CreateMap<Image, PostDto>().ForMember(destionation => destionation.ImageUrl, option => option.MapFrom(source => source.ImageUrl));
            CreateMap<Video, PostDto>().ForMember(destionation => destionation.VideoUrl, option => option.MapFrom(source => source.VideoUrl));
        }
    }
}
