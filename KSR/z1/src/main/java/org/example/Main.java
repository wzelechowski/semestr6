package org.example;

import org.jsoup.nodes.Document;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) throws IOException {
        //Document doc = new Document("C:\\Users\\Julia\\Downloads\\reuters+21578+text+categorization+collection\\reuters21578\\reut2-021.sgm");
        //List<String>
        //Reader r = new Reader("src/main/resources");
//        int count = 0;
//        for (Article a : Reader.read("src/main/resources")) {
//           System.out.println(a.getCountry() + "\n" + a.getBody());
//            count ++;
//        }
//        System.out.println(count);
        System.out.println(Reader.read("src/main/resources").get(0).getCountry() + "\n" + Reader.read("src/main/resources").get(0).getBody());
        //FeaturesExtractor feature = new FeaturesExtractor();
        System.out.println(FeaturesExtractor.countWords(Reader.read("src/main/resources").get(0)));
//        r.read("reut2-002.sgm");
    }
}