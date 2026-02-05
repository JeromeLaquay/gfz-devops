package com.gfz.mappingservice;

import com.gfz.dto.EmailData;
import com.gfz.dto.UserDto;
import com.gfz.dto.UserRequest;
import com.gfz.entity.User;
import com.gfz.mapper.UserMapper;
import com.gfz.service.EmailService;
import com.gfz.service.TokenService;
import com.gfz.service.UserService;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class UserMappingService {
    private final UserMapper userMapper;
    private final UserService userService;
    private final TokenService tokenService;
    private final EmailService emailService;
    
    @Value("${app.frontend.url:http://localhost:3000}")
    private String frontendUrl;
    
    @Value("${spring.mail.username}")
    private String fromEmail;

    public UserMappingService(UserMapper userMapper, 
                             UserService userService,
                             TokenService tokenService,
                             EmailService emailService) {
        this.userMapper = userMapper;
        this.userService = userService;
        this.tokenService = tokenService;
        this.emailService = emailService;
    }

    public UserDto create(UserRequest request) {
        User user = userMapper.toEntity(request);
        
        if (request.password() == null || request.password().isEmpty()) {
            String resetToken = tokenService.genererToken();
            user.setResetToken(resetToken);
            user.setPassword("TEMPORARY_PASSWORD");
        }
        
        User saved = userService.save(user);
        
        if (request.password() == null || request.password().isEmpty()) {
            envoyerEmailCreationCompte(saved);
        }
        
        return userMapper.toResponse(saved);
    }
    
    private void envoyerEmailCreationCompte(User user) {
        String lien = frontendUrl + "/admin/set-password?token=" + user.getResetToken();
        String message = "Bonjour " + (user.getName() != null ? user.getName() : user.getUsername()) + ",\n\n";
        message += "Un compte administrateur a été créé pour vous.\n\n";
        message += "Veuillez créer votre mot de passe en cliquant sur le lien suivant :\n";
        message += lien + "\n\n";
        message += "Cordialement,\nL'équipe GFZ Online";
        
        EmailData emailData = new EmailData(
            fromEmail,
            user.getEmail() != null ? user.getEmail() : user.getUsername(),
            user.getName() != null ? user.getName() : user.getUsername(),
            "Création de votre compte administrateur",
            message
        );
        emailService.envoyerEmail(emailData);
    }

    public List<UserDto> findAll() {
        List<User> users = userService.findAll();
        return users.stream()
            .map(userMapper::toResponse)
            .collect(Collectors.toList());
    }

    public UserDto findById(Long id) {
        User user = userService.findById(id);
        return userMapper.toResponse(user);
    }

    public void delete(Long id) {
        userService.delete(id);
    }

    public void definirMotDePasse(String token, String password) {
        userService.definirMotDePasse(token, password);
    }

    public void demanderReinitialisationMotDePasse(String emailOrUsername) {
        User user = userService.findByEmailOrUsername(emailOrUsername);
        String resetToken = tokenService.genererToken();
        user.setResetToken(resetToken);
        userService.save(user);
        envoyerEmailReinitialisation(user, resetToken);
    }

    private void envoyerEmailReinitialisation(User user, String token) {
        String lien = frontendUrl + "/reset-password?token=" + token;
        String message = "Bonjour " + (user.getName() != null ? user.getName() : user.getUsername()) + ",\n\n";
        message += "Vous avez demandé la réinitialisation de votre mot de passe.\n\n";
        message += "Cliquez sur le lien suivant pour créer un nouveau mot de passe :\n";
        message += lien + "\n\n";
        message += "Si vous n'avez pas demandé cette réinitialisation, ignorez cet email.\n\n";
        message += "Cordialement,\nL'équipe GFZ Online";
        
        String emailDestinataire = user.getEmail() != null ? user.getEmail() : user.getUsername();
        
        EmailData emailData = new EmailData(
            fromEmail,
            emailDestinataire,
            user.getName() != null ? user.getName() : user.getUsername(),
            "Réinitialisation de votre mot de passe",
            message
        );
        emailService.envoyerEmail(emailData);
    }
}
