package com.gfz.dto;

public record UserDto(
    Long id,
    String username,
    String email,
    String name
) {}
