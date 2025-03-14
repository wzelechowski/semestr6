package org.example;

import org.jsoup.Jsoup;
import java.io.File;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;


public class Reader {

    private Reader() {
    }

    //TERAZ WCZYTUJE DO BODY CALY TEKST ŁĄCZNIE Z TYTUŁEM I DATĄ ŻEBY WCZYTYWAĆ TYLKO BODY TO ODKOMENTOWAĆ BODY Z .HTML(), INDEX I IF ELSE A ZAKOMENTOWAĆ BODY Z TEXT()
    public static List<Article> read(String path) throws IOException {
        File[] files = new File(path).listFiles();

        if(files == null) {
            return null;
        }

        List<Document> documents = new ArrayList<>();

        for (File file : files) {
            documents.add(Jsoup.parse(file, "UTF-8", ""));
        }

        List<Article> articles = new ArrayList<>();
        //int count = 0;

        for (Document doc : documents) {
            for (Element element : doc.select("REUTERS")) {
                //count ++;
                //String body = element.select("TEXT").html();
                String body = element.select("TEXT").text();
                //System.out.println(body);
//                int index = body.indexOf("</dateline>".trim());
//                if (index != -1 && body.length() > index + "</dateline>".length()) {
//                    body = body.substring(index + "</dateline>".length());
//                }
//                else {
//                    index = body.indexOf("</title>".trim());
//                    if(index != -1 && body.length() > index + "</title>".length())
//                        body = body.substring(index + "</title>".length());
//                    //else {
//                        //System.out.println(body);
//                    //}
//                }
                String places = element.select("PLACES").select("D").text();
                Article article = new Article(body, places);
                if (article.getCountry().matches("west-germany|usa|france|uk|canada|japan") && !Objects.equals(article.getBody().get(0), "******")) {
                    articles.add(article);
                    //count++;
                }
            }
        }
       // System.out.println(count);
        return articles;
    }

}
