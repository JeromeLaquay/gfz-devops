package com.gfz.service;

import com.gfz.dto.EmailData;
import com.gfz.dto.NewsletterRequest;
import com.gfz.dto.NewsletterSendRequest;
import com.gfz.entity.NewsletterSubscriber;
import com.gfz.repository.NewsletterSubscriberRepository;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class NewsletterService {
    private final NewsletterSubscriberRepository repository;
    private final EmailService emailService;
    
    @Value("${spring.mail.username}")
    private String fromEmail;

    public NewsletterService(NewsletterSubscriberRepository repository, 
                           EmailService emailService) {
        this.repository = repository;
        this.emailService = emailService;
    }

    public void subscribe(NewsletterRequest request) {
        if (repository.findByEmail(request.email()).isPresent()) {
            throw new RuntimeException("Email déjà inscrit");
        }

        NewsletterSubscriber subscriber = new NewsletterSubscriber();
        subscriber.setName(request.name());
        subscriber.setEmail(request.email());
        repository.save(subscriber);
    }

    public void unsubscribe(String email) {
        NewsletterSubscriber subscriber = repository.findByEmail(email)
            .orElseThrow(() -> new RuntimeException("Email non trouvé"));
        if (subscriber != null) {
            repository.delete(subscriber);
        }
    }

    public void envoyerNewsletter(NewsletterSendRequest request) {
        List<NewsletterSubscriber> abonnes = repository.findAll();
        
        for (NewsletterSubscriber abonne : abonnes) {
            EmailData emailData = new EmailData(
                fromEmail,
                abonne.getEmail(),
                abonne.getName(),
                "Newsletter GFZ Online :" + request.sujet(),
                construireCorpsNewsletter(abonne.getName(), request.message())
            );
            emailService.envoyerEmail(emailData);
        }
    }

    private String construireCorpsNewsletter(String nom, String message) {
        return "Bonjour " + nom + ",\n\n" + message + "\n\n" + 
               "Cordialement,\nL'équipe GFZ Online";
    }
}
