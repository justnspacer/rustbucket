using AutoMapper;
using RustyTech.Server.Models.Dtos;
using RustyTech.Server.Models.Posts;

namespace RustyTech.Server.AutoMapper
{
    public class MappingProfile : Profile
    {
        public MappingProfile()
        {
            CreateMap<User, UserDto>();

            CreateMap<Post, PostDto>().ForMember(destionation => destionation.User, option => option.MapFrom(source => source.User));
            CreateMap<Post, PostDto>().ForMember(destionation => destionation.Keywords, option => option.MapFrom(source => source.Keywords));

            CreateMap<Post, PostReadDto>().ForMember(destionation => destionation.User, option => option.MapFrom(source => source.User));
            CreateMap<Post, PostReadDto>().ForMember(destionation => destionation.Keywords, option => option.MapFrom(source => source.Keywords));

            CreateMap<BlogPost, PostReadDto>();
            CreateMap<ImagePost, PostReadDto>();
            CreateMap<VideoPost, PostReadDto>();

        }
    }
}
