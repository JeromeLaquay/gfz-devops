package com.gfz.service;

import com.gfz.entity.User;
import com.gfz.repository.UserRepository;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class UserService {
    private final UserRepository repository;
    private final PasswordEncoder passwordEncoder;

    public UserService(UserRepository repository, PasswordEncoder passwordEncoder) {
        this.repository = repository;
        this.passwordEncoder = passwordEncoder;
    }

    public User save(User user) {
        if (user.getPassword() != null && 
            !user.getPassword().startsWith("$2a$") && 
            !user.getPassword().equals("TEMPORARY_PASSWORD")) {
            user.setPassword(passwordEncoder.encode(user.getPassword()));
        } else if (user.getPassword() != null && user.getPassword().equals("TEMPORARY_PASSWORD")) {
            String tempPassword = passwordEncoder.encode("TEMPORARY_PASSWORD_" + System.currentTimeMillis());
            user.setPassword(tempPassword);
        }
        return repository.save(user);
    }

    public List<User> findAll() {
        return repository.findAll();
    }

    public User findById(Long id) {
        return repository.findById(id)
            .orElseThrow(() -> new RuntimeException("Utilisateur non trouvé"));
    }

    public void delete(Long id) {
        repository.deleteById(id);
    }

    public User findByResetToken(String token) {
        return repository.findByResetToken(token)
            .orElseThrow(() -> new RuntimeException("Token invalide"));
    }

    public void definirMotDePasse(String token, String password) {
        User user = findByResetToken(token);
        user.setPassword(passwordEncoder.encode(password));
        user.setResetToken(null);
        repository.save(user);
    }

    public User findByEmailOrUsername(String emailOrUsername) {
        return repository.findByEmail(emailOrUsername)
            .orElseGet(() -> repository.findByUsername(emailOrUsername)
                .orElseThrow(() -> new RuntimeException("Utilisateur non trouvé")));
    }
}
