class Buddyhub < Formula
  desc "Standalone TUI configurator for the official Claude Code Buddy"
  homepage "https://github.com/verycafe/buddyhub"
  url "https://github.com/verycafe/buddyhub/archive/70d793fb2d060ad24bd126f77f233eaeeaedfb22.tar.gz"
  sha256 "0ef66b3fcf536de3cad56b388d77a40155e442a3da05757c0d37922d12088561"
  license "AGPL-3.0-only"

  depends_on "python@3.13"

  def install
    libexec.install Dir["*"]
    (bin/"buddyhub").write <<~SH
      #!/bin/bash
      exec "#{Formula["python@3.13"].opt_bin}/python3.13" "#{libexec}/buddyhub_tui.py" "$@"
    SH
  end

  test do
    output = shell_output("#{bin}/buddyhub --dump-language en")
    assert_match "Language", output
  end
end
