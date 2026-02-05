package com.gfz.mappingservice;

import com.gfz.dto.ArticleRequest;
import com.gfz.dto.ArticleResponse;
import com.gfz.entity.Article;
import org.springframework.stereotype.Service;
import com.gfz.mapper.ArticleMapper;
import com.gfz.service.ArticleService;
import java.util.List;
import java.util.stream.Collectors;
@Service
public class ArticleMappingService {
    private final ArticleMapper articleMapper;
    private final ArticleService articleService;

    public ArticleMappingService(ArticleMapper articleMapper, ArticleService articleService) {
        this.articleMapper = articleMapper;
        this.articleService = articleService;
    }

    public ArticleResponse create(ArticleRequest request) {
        Article article = articleMapper.toEntity(request);
        Article saved = articleService.save(article);
        return articleMapper.toResponse(saved);
    }

    public List<ArticleResponse> findAll() {
        List<Article> articles = articleService.findAll();
        return articles.stream()
            .map(articleMapper::toResponse)
            .collect(Collectors.toList());
    }

    public ArticleResponse findById(Long id) {
        Article article = articleService.findById(id);
        return articleMapper.toResponse(article);
    }

    public ArticleResponse update(Long id, ArticleRequest request) {
        Article article = articleMapper.toEntity(request);
        Article updated = articleService.update(id, article);
        return articleMapper.toResponse(updated);
    }

    public void delete(Long id) {
        articleService.delete(id);
    }
}
