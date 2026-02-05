package com.gfz.service;

import com.gfz.dto.EmailData;
import com.gfz.entity.Contact;
import com.gfz.repository.ContactRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ContactService {
    private final ContactRepository repository;
    private final EmailService emailService;

    public ContactService(ContactRepository repository, EmailService emailService) {
        this.emailService = emailService;
        this.repository = repository;
    }

    public Contact save(Contact contact) {
        return repository.save(contact);
    }

    public List<Contact> findAll() {
        return repository.findAll();
    }

    public Contact findById(Long id) {
        Contact contact = repository.findById(id)
            .orElseThrow(() -> new RuntimeException("Contact non trouvé"));
        return contact;
    }

    public void delete(Long id) {
        repository.deleteById(id);
    }

    public void sendEmail(Contact contact) {
        EmailData emailData = new EmailData(
            "laquay.jerome@gmail.com",
            contact.getEmail(),
            contact.getNom(),
            contact.getSujet(),
            contact.getMessage()
        );
        emailService.envoyerReponse(emailData);
    }
}
