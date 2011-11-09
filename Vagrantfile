Vagrant::Config.run do |config|
  config.vm.box = "lucid32"

  config.vm.define :overmind do |overmind|
    overmind.vm.forward_port("http", 80, 8080)

    overmind.vm.provision :yaybu do |config|
      config.yay = <<-EOS
        .include:
          - contrib/yaybu/web.yay
        EOS
    end
  end


  # Deploy a second empty VM that overmind can deploy to

  config.vm.define :minion do |minion|
    minion.vm.provision :yaybu do |config|
    end
  end

end
