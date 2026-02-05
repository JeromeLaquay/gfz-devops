package com.gfz.mappingservice;

import com.gfz.dto.ContactRequest;
import com.gfz.dto.ContactResponse;
import com.gfz.dto.EmailData;
import com.gfz.entity.Contact;
import com.gfz.mapper.ContactMapper;
import com.gfz.service.ContactService;
import com.gfz.service.EmailService;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class ContactMappingService {
    private final ContactMapper contactMapper;
    private final ContactService contactService;
    private final EmailService emailService;

    public ContactMappingService(ContactMapper contactMapper, 
                                 ContactService contactService,
                                 EmailService emailService) {
        this.contactMapper = contactMapper;
        this.contactService = contactService;
        this.emailService = emailService;
    }

    public ContactResponse create(ContactRequest request) {
        Contact contact = contactMapper.toEntity(request);
        Contact saved = contactService.save(contact);
        //envoyer un email à l'administrateur avec le sujet "Nouveau message de contact" et le corps "Nouveau message de contact de " + contact.getNom() + " avec l'email " + contact.getEmail() + " et le message " + contact.getMessage()
        EmailData emailData = new EmailData(
            request.email(),
            "laquay.jerome@gmail.com",
            contact.getNom(),
            "Nouveau message de contact",
            "Nouveau message de contact de " + contact.getNom() + " avec l'email " + contact.getEmail() + " et le message " + contact.getMessage()
        );
        emailService.envoyerEmail(emailData);
        if(request.reply()) {
            contactService.sendEmail(saved);
        }
        return contactMapper.toResponse(saved);
    }

    public List<ContactResponse> findAll() {
        List<Contact> contacts = contactService.findAll();
        return contacts.stream()
            .map(contactMapper::toResponse)
            .collect(Collectors.toList());
    }

    public ContactResponse findById(Long id) {
        Contact contact = contactService.findById(id);
        return contactMapper.toResponse(contact);
    }

    public void delete(Long id) {
        contactService.delete(id);
    }

    public void repondre(Long id, String messageReponse) {
        Contact contact = contactService.findById(id);
        EmailData emailData = new EmailData(
            "laquay.jerome@gmail.com",
            contact.getEmail(),
            contact.getNom(),
            contact.getSujet(),
            messageReponse
        );
        emailService.envoyerReponse(emailData);
    }
}
