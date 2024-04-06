package dev.vk.fc.modules.datapublisher;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class FCDataPublisher implements CommandLineRunner {

    private final static Logger logger = LoggerFactory.getLogger(FCDataPublisher.class);

    public static void main(String[] args) {
        SpringApplication.run(FCDataPublisher.class, args);
    }

    @Override
    public void run(String... args) throws Exception {
        logger.info("Running cmd application");
        for (String s : args) {
            logger.info("arg: {}", s);
        }
        logger.info("Finishing...");
    }
}
