package dev.vk.fc.modules.datapublisher.cmd;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class SimpleCmdRunner implements CommandLineRunner{

    private final static Logger logger = LoggerFactory.getLogger(SimpleCmdRunner.class);

    @Override
    public void run(String... args) throws Exception {
        logger.info("Running cmd application");
        for (String s : args) {
//            logger.info("arg: {}", s);
        }
//        logger.info("Finishing...");
    }
}
