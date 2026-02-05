package com.gfz.service;

import com.gfz.entity.Article;
import com.gfz.repository.ArticleRepository;
import org.springframework.stereotype.Service;
import java.util.List;


@Service
public class ArticleService {
    private final ArticleRepository repository;

    public ArticleService(ArticleRepository repository) {
        this.repository = repository;
    }

    public Article save(Article article) {
        return repository.save(article);
    }

    public Article findById(Long id) {
        Article article = repository.findById(id)
            .orElseThrow(() -> new RuntimeException("Article non trouvé"));
        return article;
    }

    public List<Article> findAll() {
        return repository.findAll();
    }

    public Article update(Long id, Article article) {
        Article existingArticle = repository.findById(id)
            .orElseThrow(() -> new RuntimeException("Article non trouvé"));
        updateArticle(article, existingArticle);
        Article saved = repository.save(existingArticle);
        return saved;
    }

    private void updateArticle(Article article, Article existingArticle) {
        existingArticle.setTitre(article.getTitre());
        existingArticle.setImage(article.getImage());
        existingArticle.setContenu(article.getContenu());
        if (article.getDateCreation() != null) {
            existingArticle.setDateCreation(article.getDateCreation());
        }
    }

    public void delete(Long id) {
        repository.deleteById(id);
    }
}
