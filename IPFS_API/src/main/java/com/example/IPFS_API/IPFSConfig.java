package com.example.IPFS_API;

import io.ipfs.api.IPFS;
import org.springframework.beans.factory.config.ConfigurableBeanFactory;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Scope;

import java.io.IOException;

@Configuration
@Scope(value = ConfigurableBeanFactory.SCOPE_SINGLETON)
public class IPFSConfig {

    IPFS ipfs;

    public IPFSConfig() throws IOException {
        // ipfs = new IPFS("/dnsaddr/ipfs.infura.io/tcp/5001/https");
        ipfs = new IPFS("/ip4/127.0.0.1/tcp/8001");
        ipfs.refs.local();
    }

}
