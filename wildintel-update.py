#!/usr/bin/env python3
"""Add read-more collapse feature to WildIntel chat widget."""

f = '/home/wildintelapp/frontend/wildintel-chat.js'
lines = open(f).readlines()
out = []
i = 0
css_done = fn_done = stream_done = False

while i < len(lines):
    line = lines[i]

    # 1. CSS: insert after .wi-msg-escalation a { ... } closing brace
    if not css_done and '.wi-msg-escalation a {' in line:
        out.append(line)
        i += 1
        while i < len(lines):
            out.append(lines[i])
            if lines[i].strip() == '}':
                break
            i += 1
        ind = lines[i][:len(lines[i]) - len(lines[i].lstrip())]
        out.append(ind + '.wi-msg-bot.wi-collapsed {\n')
        out.append(ind + '  max-height: 120px;\n')
        out.append(ind + '  overflow: hidden;\n')
        out.append(ind + '  -webkit-mask-image: linear-gradient(to bottom, #000 60%, transparent 100%);\n')
        out.append(ind + '  mask-image: linear-gradient(to bottom, #000 60%, transparent 100%);\n')
        out.append(ind + '}\n')
        out.append(ind + '.wi-read-more {\n')
        out.append(ind + '  background: none;\n')
        out.append(ind + '  border: none;\n')
        out.append(ind + '  color: #E3B341;\n')
        out.append(ind + '  cursor: pointer;\n')
        out.append(ind + '  font-size: 13px;\n')
        out.append(ind + '  padding: 2px 0 0;\n')
        out.append(ind + '  font-family: inherit;\n')
        out.append(ind + '  font-weight: 600;\n')
        out.append(ind + '}\n')
        out.append(ind + '.wi-read-more:hover { text-decoration: underline; }\n')
        css_done = True
        i += 1
        continue

    # 2. addBotMessage: add wrapper div and collapse logic
    if not fn_done and 'function addBotMessage' in line:
        out.append(line)
        i += 1
        # var c = ...
        out.append(lines[i])
        ind = lines[i][:len(lines[i]) - len(lines[i].lstrip())]
        i += 1
        # var m = ... -> add var w before it
        out.append(ind + 'var w = document.createElement("div");\n')
        out.append(lines[i])  # var m = ...
        i += 1
        out.append(lines[i])  # m.className = ...
        i += 1
        out.append(lines[i])  # m.innerHTML = ...
        i += 1
        # skip c.appendChild(m);
        i += 1
        # skip scrollToBottom();
        i += 1
        out.append(ind + 'w.appendChild(m);\n')
        out.append(ind + 'if (text && text.length > 300) {\n')
        out.append(ind + '  m.classList.add("wi-collapsed");\n')
        out.append(ind + '  var rb = document.createElement("button");\n')
        out.append(ind + '  rb.className = "wi-read-more";\n')
        out.append(ind + '  rb.textContent = "Read more ▼";\n')
        out.append(ind + '  rb.onclick = function () {\n')
        out.append(ind + '    var exp = m.classList.toggle("wi-collapsed");\n')
        out.append(ind + '    rb.textContent = exp ? "Read more ▼" : "Show less ▲";\n')
        out.append(ind + '    scrollToBottom();\n')
        out.append(ind + '  };\n')
        out.append(ind + '  w.appendChild(rb);\n')
        out.append(ind + '}\n')
        out.append(ind + 'c.appendChild(w);\n')
        out.append(ind + 'scrollToBottom();\n')
        fn_done = True
        continue

    # 3. Post-stream: after conversationHistory.push(fullText), add collapse
    if not stream_done and 'content: fullText' in line and 'push' in line:
        out.append(line)
        ind = line[:len(line) - len(line.lstrip())]
        out.append(ind + 'if (fullText.length > 300 && botMsg.parentNode) {\n')
        out.append(ind + '  botMsg.classList.add("wi-collapsed");\n')
        out.append(ind + '  var rb = document.createElement("button");\n')
        out.append(ind + '  rb.className = "wi-read-more";\n')
        out.append(ind + '  rb.textContent = "Read more ▼";\n')
        out.append(ind + '  rb.onclick = function () {\n')
        out.append(ind + '    var exp = botMsg.classList.toggle("wi-collapsed");\n')
        out.append(ind + '    rb.textContent = exp ? "Read more ▼" : "Show less ▲";\n')
        out.append(ind + '    scrollToBottom();\n')
        out.append(ind + '  };\n')
        out.append(ind + '  botMsg.parentNode.appendChild(rb);\n')
        out.append(ind + '}\n')
        stream_done = True
        i += 1
        continue

    out.append(line)
    i += 1

open(f, 'w').writelines(out)
print('CSS:', 'OK' if css_done else 'FAIL')
print('addBotMessage:', 'OK' if fn_done else 'FAIL')
print('Stream:', 'OK' if stream_done else 'FAIL')
if css_done and fn_done and stream_done:
    print('Done! WildIntel updated with read-more feature.')
else:
    print('WARNING: Some modifications failed. Check output above.')
