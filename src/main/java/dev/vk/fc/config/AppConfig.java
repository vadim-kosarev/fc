package dev.vk.fc.config;

import lombok.Data;
import lombok.Getter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

@Configuration("classpath:application.properties")
@Getter
public class AppConfig {
    @Value("${app.version.major}")
    private long versionMajor;
    @Value("${app.version.minor}")
    private long versionMinor;
    @Value("${app.version.build}")
    private long versionBuild;
}
