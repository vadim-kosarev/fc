package dev.vk.fc.modules.datapublisher.cmd;

import com.github.rvesse.airline.HelpOption;
import com.github.rvesse.airline.annotations.Cli;
import com.github.rvesse.airline.annotations.Command;
import com.github.rvesse.airline.annotations.Option;
import com.github.rvesse.airline.help.Help;
import com.github.rvesse.airline.help.*;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import javax.inject.Inject;

@Component
@Cli(name = "cmd",
        commands = {HelloWorld.HelloCmd.class, HelloWorld.ByeCmd.class, Help.class},
        defaultCommand = HelloWorld.HelloCmd.class)
public class HelloWorld implements CommandLineRunner {

    private final static Logger logger = LoggerFactory.getLogger(HelloWorld.class);

    @Override
    public void run(String... args) throws Exception {
        com.github.rvesse.airline.Cli<Runnable> cli = new com.github.rvesse.airline.Cli<Runnable>(HelloWorld.class);
        Runnable c = cli.parse(args);
        c.run();
    }

    public static abstract class Cmd implements Runnable {

        @Option(name = {"-f", "--file"}, description = "File to process")
        protected String file;

        @Inject
        protected HelpOption<Cmd> help;
    }

    @Command(name = "hello")
    public static class HelloCmd extends Cmd {

        @Override
        public void run() {
            if (help.showHelpIfRequested()) return;
            logger.info("HELLO processing  {} : ..., {}", file, this);
        }
    }

    @Command(name = "bye")
    public static class ByeCmd extends Cmd {

        @Override
        public void run() {
            if (help.showHelpIfRequested()) return;
            logger.info("BYE: ... {}", file);
        }
    }

}
