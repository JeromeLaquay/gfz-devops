package com.gfz.dto;

public record LoginResponse(
    String token,
    String type,
    UserDto user
) {
    public LoginResponse(String token, UserDto user) {
        this(token, "Bearer", user);
    }
}
