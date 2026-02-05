package com.gfz.service;

import com.gfz.dto.LoginRequest;
import com.gfz.dto.LoginResponse;
import com.gfz.dto.UserDto;
import com.gfz.entity.User;
import com.gfz.repository.UserRepository;
import com.gfz.security.JwtTokenProvider;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class AuthService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtTokenProvider jwtTokenProvider;

    public AuthService(
        UserRepository userRepository,
        PasswordEncoder passwordEncoder,
        JwtTokenProvider jwtTokenProvider
    ) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtTokenProvider = jwtTokenProvider;
    }

    public LoginResponse login(LoginRequest request) {
        System.out.println(request.username());
        User user = userRepository.findByUsername(request.username())
            .orElseThrow(() -> new RuntimeException("Utilisateur non trouvé"));
        System.out.println(user.getPassword());
        if (!passwordEncoder.matches(request.password(), user.getPassword())) {
            throw new RuntimeException("Mot de passe incorrect");
        }

        String token = jwtTokenProvider.generateToken(user.getUsername());
        UserDto userDto = new UserDto(
            user.getId(),
            user.getUsername(),
            user.getEmail(),
            user.getName()
        );

        return new LoginResponse(token, userDto);
    }
}
