package dev.vk.fc.modules.datapublisher;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class FCDataPublisher {

    private final static Logger logger = LoggerFactory.getLogger(FCDataPublisher.class);

    public static void main(String[] args) {
        SpringApplication.run(FCDataPublisher.class, args);
    }
}
