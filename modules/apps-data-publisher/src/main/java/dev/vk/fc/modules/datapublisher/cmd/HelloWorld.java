package dev.vk.fc.modules.datapublisher.cmd;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class HelloWorld implements CommandLineRunner {

    private final static Logger logger = LoggerFactory.getLogger(HelloWorld.class);

    @Override
    public void run(String... args) throws Exception {
        logger.info("Running...done");
    }
}
