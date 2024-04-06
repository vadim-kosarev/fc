package dev.vk.fc.config;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Configuration
@PropertySource("classpath:rabbitmq.properties")
public class RabbitMqConfig {
    @Value("${rabbitmq.host}")
    private String host;
    @Value("${rabbitmq.port}")
    private int port;
    @Value("${rabbitmq.user}")
    private String user;
    @Value("${rabbitmq.password}")
    private String password;
    @Value("${rabbitmq.vhost}")
    private String vhost;
}
