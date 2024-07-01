using AutoMapper;

namespace RustyTech.Server.MappingProfiles
{
    public class MappingProfile : Profile
    {
        public MappingProfile()
        {
            CreateMap<User, UserDto>();
            CreateMap<Post, PostDto>()
                .ForMember(destionation => destionation.User, option => option.MapFrom(source => source.User));
        }
    }
}
