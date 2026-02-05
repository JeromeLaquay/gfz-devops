package com.gfz.mapper;

import com.gfz.dto.UserDto;
import com.gfz.dto.UserRequest;
import com.gfz.entity.User;
import org.springframework.stereotype.Component;

@Component
public class UserMapper {
    public User toEntity(UserRequest request) {
        User user = new User();
        user.setUsername(request.username());
        user.setEmail(request.email());
        user.setPassword(request.password());
        user.setName(request.name());
        return user;
    }

    public UserDto toResponse(User user) {
        return new UserDto(
            user.getId(),
            user.getUsername(),
            user.getEmail(),
            user.getName()
        );
    }
}
