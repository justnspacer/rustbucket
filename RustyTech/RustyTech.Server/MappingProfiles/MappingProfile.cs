using AutoMapper;

namespace RustyTech.Server.MappingProfiles
{
    public class MappingProfile : Profile
    {
        public MappingProfile()
        {
            CreateMap<User, UserDto>();

            CreateMap<Post, PostDto>().ForMember(destionation => destionation.User, option => option.MapFrom(source => source.User));
            CreateMap<Post, PostDto>().ForMember(destionation => destionation.Keywords, option => option.MapFrom(source => source.Keywords.Select(post => post.KeywordId)));

            CreateMap<Blog, BlogDto>().ForMember(destionation => destionation.ImageUrls, option => option.MapFrom(source => source.ImageUrls));

            CreateMap<Image, ImageDto>().ForMember(destionation => destionation.ImageUrl, option => option.MapFrom(source => source.ImageUrl));

            CreateMap<Video, VideoDto>().ForMember(destionation => destionation.VideoUrl, option => option.MapFrom(source => source.VideoUrl));
        }
    }
}
