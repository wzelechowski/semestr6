package org.example;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Element;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class Article {
    private List<String> body;
    private String place;

    public Article(String body, String country) {
        this.body = Arrays.asList(body.replaceAll("[^a-zA-Z ]", "").trim().split("\\s+"));
        this.place = country;
    }

    public String getCountry() {
        return place;
    }

    public List<String> getBody() {
        return body;
    }



}

