package com.gfz.config;

import com.gfz.entity.User;
import com.gfz.repository.UserRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

@Component
public class DataInitializer implements CommandLineRunner {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    public DataInitializer(UserRepository userRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Override
    public void run(String... args) {
        userRepository.findByUsername("admin").ifPresentOrElse(
            existingAdmin -> {
                String encodedPassword = passwordEncoder.encode("admin123");
                if (!passwordEncoder.matches("admin123", existingAdmin.getPassword())) {
                    existingAdmin.setPassword(encodedPassword);
                    userRepository.save(existingAdmin);
                }
            },
            () -> {
                User admin = new User();
                admin.setUsername("admin");
                admin.setPassword(passwordEncoder.encode("admin123"));
                admin.setEmail("admin@gfz.fr");
                admin.setName("Administrateur");
                userRepository.save(admin);
            }
        );
    }
}
