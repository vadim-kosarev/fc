package dev.vk.fc.rest;


import dev.vk.fc.config.AppConfig;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

//@RestController
@AllArgsConstructor
public class VersionController {

    private final AppConfig appConfig;

    @GetMapping("/version")
    Version getVersion() {
        return new Version(
                appConfig.getVersionMajor(),
                appConfig.getVersionMinor(),
                appConfig.getVersionBuild(),
                appConfig.getClass()
        );
    }

    @Data
    @AllArgsConstructor
    @NoArgsConstructor
    public static class Version {
        private long major;
        private long minor;
        private long build;
        private Object msg;
    }
}
