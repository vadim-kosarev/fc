package dev.vk.fc.rest;


import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@Configuration
public class VersionController {

    @Value("${app.version.major}")
    private long versionMajor;
    @Value("${app.version.minor}")
    private long versionMinor;
    @Value("${app.version.build}")
    private long versionBuild;
    private Version version = new Version(
            versionMajor, versionMinor, versionBuild
    );

    @GetMapping("/version")
    Version getVersion() {
        return this.version;
    }

    @Data
    @AllArgsConstructor
    public static class Version {
        private long major;
        private long minor;
        private long build;
    }
}
