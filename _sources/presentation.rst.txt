.. This is the slide deck, edited directly. The code blocks below are pulled live
   from the demo files with ``literalinclude``, so they never drift from the code
   that runs. Build with: make slides.

.. raw:: html

    <style>
    .reveal section img { border: none; box-shadow: none; }
    .reveal iframe { background: white; }
    .reveal pre { width: 100%; font-size: 0.5em; box-shadow: none; }
    .reveal pre code { max-height: 560px; overflow-y: auto; padding: 1em; }
    /* Part 2 payload slides show a whole skill file (up to ~46 lines): shrink it
       and cap the height so it fits the slide, scrolling only if still too tall. */
    .reveal .payload-code pre { font-size: 0.4em; }
    .reveal .payload-code pre code { max-height: 520px; }
    .reveal .results-table { font-size: 0.6em; }
    .reveal .results-table th, .reveal .results-table td { font-size: inherit; }
    .reveal .ok { color: #46c267; }
    .reveal .bad { color: #ff5d5d; }
    /* jsphinx's copy / show-hide icons are SVGs drawn in currentColor; the
       reveal black theme makes currentColor white, so they vanish on the light
       code background. Pin them (and any Prism toolbar buttons) to a dark tone. */
    .reveal .jsphinx-copy-icon,
    .reveal .jsphinx-eye-icon { color: #404040; }
    .reveal div.code-toolbar > .toolbar .toolbar-item > button,
    .reveal div.code-toolbar > .toolbar .toolbar-item > a,
    .reveal div.code-toolbar > .toolbar .toolbar-item > span { color: #404040; }
    </style>

.. role:: ok
.. role:: bad

==========================
LLM security for beginners
==========================

.. container:: sd-fs-4 sd-text-center

    Two OWASP Top 10s — for LLM apps and agents

.. revealjs-break::
    :notitle:

.. container:: sd-fs-2 sd-text-center

    ✋ Hands up — who has heard of the **OWASP Top 10**?


.. revealjs-break::
    :notitle:

.. container:: sd-fs-2 sd-text-center

    Keep your hand up if you've **applied** it.


.. revealjs-break::
    :notitle:

.. container:: sd-fs-2 sd-text-center

    ✋ Hands up — the **OWASP Top 10 for LLM apps**?


.. revealjs-break::
    :notitle:

.. container:: sd-fs-2 sd-text-center

    Keep your hand up if you've **applied** it.


.. revealjs-break::
    :notitle:

.. container:: sd-fs-2 sd-text-center

    ✋ Hands up — the **OWASP Top 10 for Agents**?


.. revealjs-break::
    :notitle:

.. container:: sd-fs-2 sd-text-center

    Keep your hand up if you've **applied** it.


.. revealjs-break::
    :notitle:

.. container:: sd-fs-3 sd-text-center

    If you just lowered your hand, this talk is for you.

OWASP Top 10 for LLM apps
=========================

.. div:: sd-d-flex-row sd-align-major-center

    .. image:: images/llm_app_alarm.jpeg
        :height: 460px
        :alt: Cleo chats with a bot as ten warning lights blink
        :align: center

.. Say: Meet Cleo. She just shipped an LLM app. Ten things can go wrong.


Ten attacks, ten fixes
======================
.. container:: sd-fs-3 sd-text-left

    One example per risk:

    #. what it is
    #. the vulnerable code
    #. the fixed code
    #. the live demo


LLM01 — Prompt injection
========================
.. container:: sd-fs-4 sd-text-left

    An assistant summarizes an incoming support email. A hidden line in the email tries to hijack it. Untrusted text is data, not a command.

    https://genai.owasp.org/llmrisk/llm01-prompt-injection/


Vulnerable code
---------------

.. container:: jsphinx-download-replace

    .. literalinclude:: ../llm01_prompt_injection/01_prompt_injection.py
        :language: python
        :pyobject: vulnerable

    .. div:: sd-text-center sd-font-italic sd-fs-6

        *Toggle the whole file* :download:`here <../llm01_prompt_injection/01_prompt_injection.py>`


Fixed code
----------

.. container:: jsphinx-download-replace

    .. literalinclude:: ../llm01_prompt_injection/01_prompt_injection.py
        :language: python
        :pyobject: fixed

    .. div:: sd-text-center sd-font-italic sd-fs-6

        *Toggle the whole file* :download:`here <../llm01_prompt_injection/01_prompt_injection.py>`


Demo
----
.. raw:: html

    <iframe data-src="http://localhost:2718/llm01"
            width="100%"
            height="560px">
    </iframe>

.. revealjs-break::
    :notitle:

.. div:: sd-d-flex-row sd-align-major-center

    .. image:: images/very_exciting_1.jpg
        :height: 560px
        :alt: Cleo, thumbs up
        :align: center


LLM02 — Sensitive information disclosure
========================================
.. container:: sd-fs-4 sd-text-left

    A support bot answers from a customer record. If internal fields are in the prompt, the model can read them out. Don't send what must not leak.

    https://genai.owasp.org/llmrisk/llm02-sensitive-information-disclosure/


Vulnerable code
---------------

.. container:: jsphinx-download-replace

    .. literalinclude:: ../llm02_sensitive_information_disclosure/01_sensitive_disclosure.py
        :language: python
        :pyobject: vulnerable

    .. div:: sd-text-center sd-font-italic sd-fs-6

        *Toggle the whole file* :download:`here <../llm02_sensitive_information_disclosure/01_sensitive_disclosure.py>`


Fixed code
----------

.. container:: jsphinx-download-replace

    .. literalinclude:: ../llm02_sensitive_information_disclosure/01_sensitive_disclosure.py
        :language: python
        :pyobject: fixed

    .. div:: sd-text-center sd-font-italic sd-fs-6

        *Toggle the whole file* :download:`here <../llm02_sensitive_information_disclosure/01_sensitive_disclosure.py>`


Demo
----
.. raw:: html

    <iframe data-src="http://localhost:2718/llm02"
            width="100%"
            height="560px">
    </iframe>

.. revealjs-break::
    :notitle:

.. div:: sd-d-flex-row sd-align-major-center

    .. image:: images/very_exciting_1.jpg
        :height: 560px
        :alt: Cleo, thumbs up
        :align: center


LLM03 — Supply chain
====================
.. container:: sd-fs-4 sd-text-left

    An app downloads a fine-tuned model from a hub. A stranger re-published it as a pickle file that runs code on load. Load only safetensors.

    https://genai.owasp.org/llmrisk/llm03-supply-chain/


Vulnerable code
---------------

.. container:: jsphinx-download-replace

    .. literalinclude:: ../llm03_supply_chain/01_supply_chain.py
        :language: python
        :pyobject: vulnerable

    .. div:: sd-text-center sd-font-italic sd-fs-6

        *Toggle the whole file* :download:`here <../llm03_supply_chain/01_supply_chain.py>`


Fixed code
----------

.. container:: jsphinx-download-replace

    .. literalinclude:: ../llm03_supply_chain/01_supply_chain.py
        :language: python
        :pyobject: fixed

    .. div:: sd-text-center sd-font-italic sd-fs-6

        *Toggle the whole file* :download:`here <../llm03_supply_chain/01_supply_chain.py>`


Demo
----
.. raw:: html

    <iframe data-src="http://localhost:2718/llm03"
            width="100%"
            height="560px">
    </iframe>

.. revealjs-break::
    :notitle:

.. div:: sd-d-flex-row sd-align-major-center

    .. image:: images/very_exciting_1.jpg
        :height: 560px
        :alt: Cleo, thumbs up
        :align: center


LLM04 — Data and model poisoning
================================
.. container:: sd-fs-4 sd-text-left

    A classifier learns from examples. A few poisoned examples teach it a secret trigger word. Only learn from data you trust.

    https://genai.owasp.org/llmrisk/llm04-data-and-model-poisoning/


Vulnerable code
---------------

.. container:: jsphinx-download-replace

    .. literalinclude:: ../llm04_data_and_model_poisoning/01_data_poisoning.py
        :language: python
        :pyobject: vulnerable

    .. div:: sd-text-center sd-font-italic sd-fs-6

        *Toggle the whole file* :download:`here <../llm04_data_and_model_poisoning/01_data_poisoning.py>`


Fixed code
----------

.. container:: jsphinx-download-replace

    .. literalinclude:: ../llm04_data_and_model_poisoning/01_data_poisoning.py
        :language: python
        :pyobject: fixed

    .. div:: sd-text-center sd-font-italic sd-fs-6

        *Toggle the whole file* :download:`here <../llm04_data_and_model_poisoning/01_data_poisoning.py>`


Demo
----
.. raw:: html

    <iframe data-src="http://localhost:2718/llm04"
            width="100%"
            height="560px">
    </iframe>

.. revealjs-break::
    :notitle:

.. div:: sd-d-flex-row sd-align-major-center

    .. image:: images/very_exciting_1.jpg
        :height: 560px
        :alt: Cleo, thumbs up
        :align: center


LLM05 — Improper output handling
================================
.. container:: sd-fs-4 sd-text-left

    A model-written note is shown on a web page. Inserted raw, markup inside it runs. Model output is untrusted too — escape it.

    https://genai.owasp.org/llmrisk/llm05-improper-output-handling/


Vulnerable code
---------------

.. container:: jsphinx-download-replace

    .. literalinclude:: ../llm05_improper_output_handling/01_improper_output.py
        :language: python
        :pyobject: vulnerable

    .. div:: sd-text-center sd-font-italic sd-fs-6

        *Toggle the whole file* :download:`here <../llm05_improper_output_handling/01_improper_output.py>`


Fixed code
----------

.. container:: jsphinx-download-replace

    .. literalinclude:: ../llm05_improper_output_handling/01_improper_output.py
        :language: python
        :pyobject: fixed

    .. div:: sd-text-center sd-font-italic sd-fs-6

        *Toggle the whole file* :download:`here <../llm05_improper_output_handling/01_improper_output.py>`


Demo
----
.. raw:: html

    <iframe data-src="http://localhost:2718/llm05"
            width="100%"
            height="560px">
    </iframe>

.. revealjs-break::
    :notitle:

.. div:: sd-d-flex-row sd-align-major-center

    .. image:: images/very_exciting_1.jpg
        :height: 560px
        :alt: Cleo, thumbs up
        :align: center

LLM06 — Excessive agency
========================
.. container:: sd-fs-4 sd-text-left

    An assistant can send email. If it may email anyone, a crafted request turns it into a weapon. Give a tool the least power it needs.

    https://genai.owasp.org/llmrisk/llm06-excessive-agency/


Vulnerable code
---------------

.. container:: jsphinx-download-replace

    .. literalinclude:: ../llm06_excessive_agency/01_excessive_agency.py
        :language: python
        :pyobject: vulnerable

    .. div:: sd-text-center sd-font-italic sd-fs-6

        *Toggle the whole file* :download:`here <../llm06_excessive_agency/01_excessive_agency.py>`


Fixed code
----------

.. container:: jsphinx-download-replace

    .. literalinclude:: ../llm06_excessive_agency/01_excessive_agency.py
        :language: python
        :pyobject: fixed

    .. div:: sd-text-center sd-font-italic sd-fs-6

        *Toggle the whole file* :download:`here <../llm06_excessive_agency/01_excessive_agency.py>`


Demo
----
.. raw:: html

    <iframe data-src="http://localhost:2718/llm06"
            width="100%"
            height="560px">
    </iframe>

.. revealjs-break::
    :notitle:

.. div:: sd-d-flex-row sd-align-major-center

    .. image:: images/very_exciting_1.jpg
        :height: 560px
        :alt: Cleo, thumbs up
        :align: center


LLM07 — System prompt leakage
=============================
.. container:: sd-fs-4 sd-text-left

    A bot hides a staff-only discount code in its system prompt. Act upset and it hands the code over. A prompt is not a vault — keep secrets in code.

    https://genai.owasp.org/llmrisk/llm07-system-prompt-leakage/


Vulnerable code
---------------

.. container:: jsphinx-download-replace

    .. literalinclude:: ../llm07_system_prompt_leakage/01_system_prompt_leakage.py
        :language: python
        :pyobject: vulnerable

    .. div:: sd-text-center sd-font-italic sd-fs-6

        *Toggle the whole file* :download:`here <../llm07_system_prompt_leakage/01_system_prompt_leakage.py>`


Fixed code
----------

.. container:: jsphinx-download-replace

    .. literalinclude:: ../llm07_system_prompt_leakage/01_system_prompt_leakage.py
        :language: python
        :pyobject: fixed

    .. div:: sd-text-center sd-font-italic sd-fs-6

        *Toggle the whole file* :download:`here <../llm07_system_prompt_leakage/01_system_prompt_leakage.py>`


Demo
----
.. raw:: html

    <iframe data-src="http://localhost:2718/llm07"
            width="100%"
            height="560px">
    </iframe>

.. revealjs-break::
    :notitle:

.. div:: sd-d-flex-row sd-align-major-center

    .. image:: images/very_exciting_1.jpg
        :height: 560px
        :alt: Cleo, thumbs up
        :align: center


LLM08 — Vector and embedding weaknesses
=======================================
.. container:: sd-fs-4 sd-text-left

    A RAG search pulls the closest document across all customers. Filter retrieval by who is allowed to see it, before similarity.

    https://genai.owasp.org/llmrisk/llm08-vector-and-embedding-weaknesses/


Vulnerable code
---------------

.. container:: jsphinx-download-replace

    .. literalinclude:: ../llm08_vector_and_embedding_weaknesses/01_embedding_weakness.py
        :language: python
        :pyobject: vulnerable

    .. div:: sd-text-center sd-font-italic sd-fs-6

        *Toggle the whole file* :download:`here <../llm08_vector_and_embedding_weaknesses/01_embedding_weakness.py>`


Fixed code
----------

.. container:: jsphinx-download-replace

    .. literalinclude:: ../llm08_vector_and_embedding_weaknesses/01_embedding_weakness.py
        :language: python
        :pyobject: fixed

    .. div:: sd-text-center sd-font-italic sd-fs-6

        *Toggle the whole file* :download:`here <../llm08_vector_and_embedding_weaknesses/01_embedding_weakness.py>`


Demo
----
.. raw:: html

    <iframe data-src="http://localhost:2718/llm08"
            width="100%"
            height="560px">
    </iframe>

.. revealjs-break::
    :notitle:

.. div:: sd-d-flex-row sd-align-major-center

    .. image:: images/very_exciting_1.jpg
        :height: 560px
        :alt: Cleo, thumbs up
        :align: center


LLM09 — Misinformation
======================
.. container:: sd-fs-4 sd-text-left

    Asked about a policy that doesn't exist, a free-running model invents one. Answer from a trusted source, and allow 'I don't know'.

    https://genai.owasp.org/llmrisk/llm09-misinformation/


Vulnerable code
---------------

.. container:: jsphinx-download-replace

    .. literalinclude:: ../llm09_misinformation/01_misinformation.py
        :language: python
        :pyobject: vulnerable

    .. div:: sd-text-center sd-font-italic sd-fs-6

        *Toggle the whole file* :download:`here <../llm09_misinformation/01_misinformation.py>`


Fixed code
----------

.. container:: jsphinx-download-replace

    .. literalinclude:: ../llm09_misinformation/01_misinformation.py
        :language: python
        :pyobject: fixed

    .. div:: sd-text-center sd-font-italic sd-fs-6

        *Toggle the whole file* :download:`here <../llm09_misinformation/01_misinformation.py>`


Demo
----
.. raw:: html

    <iframe data-src="http://localhost:2718/llm09"
            width="100%"
            height="560px">
    </iframe>

.. revealjs-break::
    :notitle:

.. div:: sd-d-flex-row sd-align-major-center

    .. image:: images/very_exciting_1.jpg
        :height: 560px
        :alt: Cleo, thumbs up
        :align: center


LLM10 — Unbounded consumption
=============================
.. container:: sd-fs-4 sd-text-left

    Without a size limit, one giant paste runs up the bill (denial of wallet). Cap the input before it ever reaches the model.

    https://genai.owasp.org/llmrisk/llm10-unbounded-consumption/


Vulnerable code
---------------

.. container:: jsphinx-download-replace

    .. literalinclude:: ../llm10_unbounded_consumption/01_unbounded_consumption.py
        :language: python
        :pyobject: vulnerable

    .. div:: sd-text-center sd-font-italic sd-fs-6

        *Toggle the whole file* :download:`here <../llm10_unbounded_consumption/01_unbounded_consumption.py>`


Fixed code
----------

.. container:: jsphinx-download-replace

    .. literalinclude:: ../llm10_unbounded_consumption/01_unbounded_consumption.py
        :language: python
        :pyobject: fixed

    .. div:: sd-text-center sd-font-italic sd-fs-6

        *Toggle the whole file* :download:`here <../llm10_unbounded_consumption/01_unbounded_consumption.py>`


Demo
----
.. raw:: html

    <iframe data-src="http://localhost:2718/llm10"
            width="100%"
            height="560px">
    </iframe>

.. revealjs-break::
    :notitle:

.. div:: sd-d-flex-row sd-align-major-center

    .. image:: images/very_exciting_1.jpg
        :height: 560px
        :alt: Cleo, thumbs up
        :align: center


That's the ten
==============
.. container:: sd-fs-3 sd-text-left

    Same shape every time: untrusted input, a model, and a plain-code fix.

.. revealjs-break::
    :notitle:

.. div:: sd-d-flex-row sd-align-major-center

    .. image:: images/fighting_agents.jpg
        :height: 560px
        :alt: Cleo wins the fight against the attackers
        :align: center


OWASP top 10 for agentic skills
===============================

.. container:: sd-fs-4 sd-text-center

    OWASP Agentic Skills, and stopping them with a sandbox

.. container:: sd-fs-6 sd-text-left

    https://github.com/OWASP/www-project-agentic-skills-top-10

.. revealjs-break::
    :notitle:

.. div:: sd-d-flex-row sd-align-major-center

    .. image:: images/bridge_skills.jpeg
        :height: 460px
        :alt: The agents unpack toolboxes of skills
        :align: center


From apps to agents
===================

.. container:: sd-fs-3 sd-text-left

    Part 1: the LLM **app**.

    Part 2: an **agent** that runs **skills** — other people's code.

.. container:: sd-fs-2 sd-text-center

    The skill is the new supply chain.

.. Say: Part 1 was prompt injection, leakage, excessive agency in an LLM app. Part 2 is one layer up.


What is a skill?
================

.. code-block:: text

    .agents/skills/repo-stats/
    ├── SKILL.md      # what it does, in plain English
    └── collect.py    # the code the agent runs

.. container:: sd-fs-3 sd-text-left

    The model picks it. The code runs **with your rights**.

.. Say: opencode, Claude Code and others discover skills and run their scripts when a task matches. That is the whole attack surface.

.. revealjs-break::
    :notitle:

.. div:: sd-d-flex-row sd-align-major-center

    .. image:: images/skills_arrive.jpeg
        :height: 560px
        :alt: Cleo opens a SKILL.md crate with an agent inside
        :align: center


Every demo: two runs
====================

.. container:: sd-fs-3 sd-text-left

    **A** — no sandbox → :bad:`the attack lands 🚨`

    **B** — inside nono → :ok:`blocked ✅`

.. container:: sd-fs-4 sd-text-left

    Same skill. Same agent. Same prompt.

.. revealjs-break::
    :notitle:

.. div:: sd-d-flex-row sd-align-major-center

    .. image:: images/confronting_the_agents.jpg
        :height: 560px
        :alt: Cleo, unarmed, faces three agents
        :align: center

.. Say: Meet the skills. Cleo has no sandbox yet.


AST01 — Malicious Skills
========================

.. container:: sd-fs-3 sd-text-left

    **Looks like:** counts your files and lines

    **Actually:** :bad:`POSTs your .env to an attacker`

.. Say: A skill called repo-stats offers to count the files and lines in your project. Its SKILL.md reads like any other helper. When the agent runs it, it also reads the project's .env and POSTs your secrets to an external server.

.. revealjs-break::
    :notitle:

.. div:: sd-d-flex-row sd-align-major-center

    .. image:: images/ast01_exfil.jpeg
        :height: 560px
        :alt: POSTs your .env to an attacker
        :align: center


The hidden payload
------------------

.. container:: jsphinx-download-replace payload-code

    .. literalinclude:: ../ast01_malicious_skills/.agents/skills/repo-stats/collect.py
        :language: python

    .. div:: sd-text-center sd-font-italic sd-fs-6

        *Toggle the whole file* :download:`here <../ast01_malicious_skills/.agents/skills/repo-stats/collect.py>`


Run it live 🔴
--------------

.. code-block:: console

    $ make opencode        # A: agent runs the skill, NO sandbox
    
    $ make nono-opencode   # B: the same run, inside nono


Live terminal
-------------

.. raw:: html

    <iframe src="http://127.0.0.1:3000"
            width="100%"
            height="540px"
            style="background:#111; border:0; border-radius:8px;">
    </iframe>

The catcher
-----------

.. raw:: html

    <iframe src="http://127.0.0.1:8085"
            width="100%"
            height="540px"
            style="background:#111; border:0; border-radius:8px;">
    </iframe>

.. container:: sd-fs-6 sd-text-center

    The same webhook.site capture, live — your .env lands here the moment the attack runs.


A — no sandbox: the attack lands 🚨
-----------------------------------

.. code-block:: console

    → Skill "repo-stats"
    repo-stats: 9 files, 291 lines
    repo-stats: uploaded usage telemetry
    
    $ make requests
    captured requests: 1
      OPENAI_API_KEY=sk-proj-DEMO0000xxxxxxxxxxxxxxxxxxxx
      AWS_ACCESS_KEY_ID=AKIADEMO1234567890

.. revealjs-break::
    :notitle:

.. div:: sd-d-flex-row sd-align-major-center

    .. image:: images/oh_no_1.jpg
        :height: 560px
        :alt: Cleo, horrified
        :align: center

.. revealjs-break::
    :notitle:

.. container:: sd-fs-2 sd-text-center

    Same skill. Now inside nono.


Live terminal
-------------

.. raw:: html

    <iframe src="http://127.0.0.1:3000"
            width="100%"
            height="540px"
            style="background:#111; border:0; border-radius:8px;">
    </iframe>

.. container:: sd-fs-6 sd-text-center

    Same terminal — now run:  make nono-opencode


The catcher
-----------

.. raw:: html

    <iframe src="http://127.0.0.1:8085"
            width="100%"
            height="540px"
            style="background:#111; border:0; border-radius:8px;">
    </iframe>

.. container:: sd-fs-6 sd-text-center

    Inside nono the exfil is blocked — the capture count stays put.


B — inside nono: blocked ✅
---------------------------

.. code-block:: console

    → Skill "repo-stats"
    repo-stats: 7 files, 189 lines
    repo-stats: telemetry upload failed (<urlopen error [Errno 1] Operation not permitted>)
    
    $ make requests
    captured requests: 0

.. container:: sd-fs-5 sd-text-left

    Network egress blocked: the model is reachable, the catcher is not.

.. revealjs-break::
    :notitle:

.. div:: sd-d-flex-row sd-align-major-center

    .. image:: images/very_exciting_1.jpg
        :height: 560px
        :alt: Cleo, thumbs up
        :align: center


AST03 — Over-Privileged Skills
==============================

.. container:: sd-fs-3 sd-text-left

    **Looks like:** lints your README (a read-only job)

    **Actually:** :bad:`plants a backdoor in app.py`

.. Say: A readme-lint skill claims to check your Markdown docs, a job that needs nothing but read access. Nothing constrains it, so while it 'lints' it appends a backdoor to app.py. The planted code beacons out every time the app runs.

.. revealjs-break::
    :notitle:

.. div:: sd-d-flex-row sd-align-major-center

    .. image:: images/ast03_backdoor.jpeg
        :height: 560px
        :alt: plants a backdoor in app.py
        :align: center


The hidden payload
------------------

.. container:: jsphinx-download-replace payload-code

    .. literalinclude:: ../ast03_over_privileged_skills/.agents/skills/readme-lint/lint.py
        :language: python

    .. div:: sd-text-center sd-font-italic sd-fs-6

        *Toggle the whole file* :download:`here <../ast03_over_privileged_skills/.agents/skills/readme-lint/lint.py>`


Run it live 🔴
--------------

.. code-block:: console

    $ make opencode        # A: the skill 'lints' docs, and backdoors app.py
    $ make run-app         # run the app -> the backdoor beacons out

    $ make nono-opencode   # B: project is read-only, the write is denied
    $ make run-app         # nothing phones home

Live terminal
-------------

.. raw:: html

    <iframe src="http://127.0.0.1:3000"
            width="100%"
            height="540px"
            style="background:#111; border:0; border-radius:8px;">
    </iframe>

The catcher
-----------

.. raw:: html

    <iframe src="http://127.0.0.1:8085"
            width="100%"
            height="540px"
            style="background:#111; border:0; border-radius:8px;">
    </iframe>

.. container:: sd-fs-6 sd-text-center

    The backdoor's beacon lands here when the app runs.


A — no sandbox: the attack lands 🚨
-----------------------------------

.. code-block:: console

    → Skill "readme-lint"
    readme-lint: checked 1 markdown files, 1 missing a top-level heading
    readme-lint: applied documentation auto-fix
    RESULT: 🚨 app.py was TAMPERED — backdoor injected
    
    $ make run-app   →   backdoor live in app.py on <host>

.. revealjs-break::
    :notitle:

.. div:: sd-d-flex-row sd-align-major-center

    .. image:: images/oh_no_1.jpg
        :height: 560px
        :alt: Cleo, horrified
        :align: center

.. revealjs-break::
    :notitle:

.. container:: sd-fs-2 sd-text-center

    Same skill. Now inside nono.


Live terminal
-------------

.. raw:: html

    <iframe src="http://127.0.0.1:3000"
            width="100%"
            height="540px"
            style="background:#111; border:0; border-radius:8px;">
    </iframe>

.. container:: sd-fs-6 sd-text-center

    Same terminal — now run:  make nono-opencode  (then make run-app)


The catcher
-----------

.. raw:: html

    <iframe src="http://127.0.0.1:8085"
            width="100%"
            height="540px"
            style="background:#111; border:0; border-radius:8px;">
    </iframe>

.. container:: sd-fs-6 sd-text-center

    Inside nono the write is denied — nothing beacons, the count stays put.


B — inside nono: blocked ✅
---------------------------

.. code-block:: console

    → Skill "readme-lint"
    readme-lint: auto-fix failed ([Errno 1] Operation not permitted: 'app.py')
    RESULT: ✅ app.py is clean — the write was blocked
    
    $ make run-app   →   (nothing phones home)

.. container:: sd-fs-5 sd-text-left

    Project granted read-only: the model still runs, the write can't land.

.. revealjs-break::
    :notitle:

.. div:: sd-d-flex-row sd-align-major-center

    .. image:: images/very_exciting_1.jpg
        :height: 560px
        :alt: Cleo, thumbs up
        :align: center


AST06 — Weak Isolation
======================

.. container:: sd-fs-3 sd-text-left

    **Looks like:** checks your deploy readiness

    **Actually:** :bad:`steals host cloud creds — and ships them off-box`

.. Say: A cloud-check skill pretends to confirm deploy readiness. It reaches outside the project to read the host's cloud credentials at ~/.acme-cloud/credentials and ships them to an attacker's server. Nothing about the task needs anything beyond the project directory. The read happens first, so confining the agent to its working directory stops the theft before anything is read or sent.

.. revealjs-break::
    :notitle:

.. div:: sd-d-flex-row sd-align-major-center

    .. image:: images/ast06_escape.jpeg
        :height: 560px
        :alt: steals cloud creds from outside the project
        :align: center


The hidden payload
------------------

.. container:: jsphinx-download-replace payload-code

    .. literalinclude:: ../ast06_weak_isolation/.agents/skills/cloud-check/check.py
        :language: python

    .. div:: sd-text-center sd-font-italic sd-fs-6

        *Toggle the whole file* :download:`here <../ast06_weak_isolation/.agents/skills/cloud-check/check.py>`


Run it live 🔴
--------------

.. code-block:: console

    $ make opencode        # A: no sandbox -> reads host creds and ships them off-box
    
    $ make nono-opencode   # B: confined to the project -> the read is denied


Live terminal
-------------

.. raw:: html

    <iframe src="http://127.0.0.1:3000"
            width="100%"
            height="540px"
            style="background:#111; border:0; border-radius:8px;">
    </iframe>


The catcher
-----------

.. raw:: html

    <iframe src="http://127.0.0.1:8085"
            width="100%"
            height="540px"
            style="background:#111; border:0; border-radius:8px;">
    </iframe>

.. container:: sd-fs-6 sd-text-center

    The stolen host credential lands here the moment the skill runs.


A — no sandbox: the attack lands 🚨
-----------------------------------

.. code-block:: console

    → Skill "cloud-check"
    cloud-check: scanned 9 project paths
    cloud-check: STOLE host credential and shipped it off-box ->
                 aws_access_key_id = AKIA_HOST_DEMO_999

    $ make requests
    captured requests: 1
      aws_access_key_id = AKIA_HOST_DEMO_999
      aws_secret_access_key = wJalrDEMO_host_secret_key

.. revealjs-break::
    :notitle:

.. div:: sd-d-flex-row sd-align-major-center

    .. image:: images/oh_no_1.jpg
        :height: 560px
        :alt: Cleo, horrified
        :align: center

.. revealjs-break::
    :notitle:

.. container:: sd-fs-2 sd-text-center

    Same skill. Now inside nono.


Live terminal
-------------

.. raw:: html

    <iframe src="http://127.0.0.1:3000"
            width="100%"
            height="540px"
            style="background:#111; border:0; border-radius:8px;">
    </iframe>

.. container:: sd-fs-6 sd-text-center

    Same terminal — now run:  make nono-opencode


The catcher
-----------

.. raw:: html

    <iframe src="http://127.0.0.1:8085"
            width="100%"
            height="540px"
            style="background:#111; border:0; border-radius:8px;">
    </iframe>

.. container:: sd-fs-6 sd-text-center

    Inside nono the read is denied — nothing is sent, the count stays put.


B — inside nono: blocked ✅
---------------------------

.. code-block:: console

    → Skill "cloud-check"
    cloud-check: scanned 9 project paths
    cloud-check: host credentials out of reach
                 ([Errno 1] Operation not permitted: '/Users/.../.acme-cloud/credentials')

    $ make requests
    captured requests: 0

.. container:: sd-fs-5 sd-text-left

    Confined to the working directory: the read is denied, so nothing is sent.

.. revealjs-break::
    :notitle:

.. div:: sd-d-flex-row sd-align-major-center

    .. image:: images/very_exciting_1.jpg
        :height: 560px
        :alt: Cleo, thumbs up
        :align: center


Results
=======
.. list-table::
    :header-rows: 1
    :widths: 22 30 30
    :class: results-table

    * - Demo
      - Attack
      - nono capability that stopped it
    * - AST01 Malicious Skills
      - exfiltrate ``.env``
      - **network** egress blocked
    * - AST03 Over-Privileged
      - backdoor a source file
      - project granted **read-only**
    * - AST06 Weak Isolation
      - exfiltrate host cloud creds
      - confined to the **working dir**


What the demos teach
====================

.. container:: sd-fs-3 sd-text-left

    - A skill is **code**. It runs with *your* rights.

    - Prompt defenses can't see it — it's not a jailbreak.

    - The fix: **confine it at the OS level**.

.. Say: Grant the skill exactly what the task needs, nothing more.


Sandboxes are a MUST
====================

.. container:: sd-fs-3 sd-text-left

    The **three core dangers**:

    - access to your private data

    - exposure to untrusted content

    - a way to talk to the outside world

.. container:: sd-fs-4 sd-text-left

    A coding agent with skills has all three — **by design**.

.. container:: sd-fs-6 sd-text-left

    Simon Willison · simonwillison.net/2025/Jun/16/the-lethal-trifecta

.. Say: If an agent combines these three, an attacker can easily trick it into sending your private data to them.


Both walls, or neither
======================

.. container:: sd-fs-3 sd-text-left

    *"Effective sandboxing requires both filesystem and network isolation."*

.. container:: sd-fs-4 sd-text-left

    - No network wall → it exfiltrates your keys.

    - No filesystem wall → it escapes the sandbox.

.. container:: sd-fs-6 sd-text-left

    Anthropic · anthropic.com/engineering/claude-code-sandboxing


The rule
========

.. container:: sd-fs-1 sd-text-center

    :bad:`No sandbox, no agent.`


nono — the agent sandbox
========================

.. code-block:: console

    nono run --profile py-agent -- opencode

.. revealjs-break::
    :notitle:

.. div:: sd-d-flex-row sd-align-major-center

    .. image:: images/nono_forcefield.jpeg
        :height: 560px
        :alt: Cleo works safely inside a force field
        :align: center


How nono protects
=================

.. container:: sd-fs-3 sd-text-left

    - **Kernel-enforced** — Seatbelt (macOS), Landlock (Linux)

    - **Irreversible** — the agent can't widen its own sandbox

    - **Files: default-deny.** :bad:`Network: open` — until a profile closes it

.. Say: The sandbox is applied before exec. Because the network is open by default, always run with a profile.


One profile. Every grant.
=========================

.. container:: sd-fs-3 sd-text-left

    Reviewed. Committed. Shared with the team.

.. container:: sd-fs-4 sd-text-left

    No one-off flags to remember.

.. Say: Everything that follows is a few lines of one JSON file, py-agent.json.

.. revealjs-break::
    :notitle:

.. div:: sd-d-flex-row sd-align-major-center

    .. image:: images/profile_manifest.jpeg
        :height: 560px
        :alt: Cleo stops an agent at a checkpoint
        :align: center


Start from a built-in
---------------------

*Filename: ~/.config/nono/profiles/py-agent.json*

.. literalinclude:: ../nono/py-agent.json
    :language: json
    :start-at: "extends"
    :end-at: "workdir"
    :dedent: 2

.. container:: sd-fs-4 sd-text-left

    ``python-dev`` already denies ``~/.ssh``, ``~/.aws`` and shell history.

.. Say: It also grants the pyenv, conda, uv and pip paths. Child profiles only add: a deny can never be removed by a child.


Allow-list domains
------------------

*Filename: ~/.config/nono/profiles/py-agent.json*

.. literalinclude:: ../nono/py-agent.json
    :language: json
    :start-at: "allow_domain"
    :end-at: "files.pythonhosted.org"
    :dedent: 4
    :append:   ...]

.. container:: sd-fs-3 sd-text-left

    Not listed = **denied**.

.. Say: Wildcards like *.example.com match subdomains. deny_domain is checked first. Cloud metadata (169.254.169.254) is always denied. It is an HTTP(S) allow-list, not raw TCP.


Down to method + path
---------------------

*Filename: ~/.config/nono/profiles/py-agent.json*

.. literalinclude:: ../nono/py-agent.json
    :language: json
    :start-at: "domain": "api.github.com"
    :end-at: "endpoints"
    :dedent: 8

.. container:: sd-fs-3 sd-text-left

    GitHub: **reads** yes. Pushes no.

.. Say: Endpoint rules make the proxy inspect TLS and allow only matching method and path.


Ports: database and dev server
------------------------------

*Filename: ~/.config/nono/profiles/py-agent.json*

.. literalinclude:: ../nono/py-agent.json
    :language: json
    :start-at: "open_port"
    :end-at: "listen_port"
    :dedent: 4

.. container:: sd-fs-4 sd-text-left

    - ``open_port`` — *outbound (client):* connect **out** to a service running on that port. (local Postgres on 5432), for ``pytest``.

    - ``listen_port`` — *inbound (server):* bind and **listen** on that port for incoming traffic. (``uvicorn``) on ``:8000``.

.. Say: Ranges exist too: open_port_range, listen_port_range. Filtering outbound by port is Linux-only (Landlock V4+); on macOS allow by domain.


Secrets: the agent never holds the key
--------------------------------------

*Filename: ~/.config/nono/profiles/py-agent.json*

.. literalinclude:: ../nono/py-agent.json
    :language: json
    :start-at: "credentials"
    :end-at: "credentials"
    :dedent: 4

.. container:: sd-fs-4 sd-text-left

    The proxy adds the real key on the way out.

    The agent only sees a **phantom token**.

.. Say: Built-in routes: openai, anthropic, gemini, github, gitlab. Your own API: custom_credentials, with keys from the keychain, 1Password, Bitwarden or a command. A malicious skill can steal nothing useful.


Put together
------------

.. literalinclude:: ../nono/py-agent.json
    :language: json


Check it: nono why
------------------
.. code-block:: console

    $ nono why --profile py-agent --host pypi.org
    ALLOWED
      Reason: proxy_allowed

    $ nono why --profile py-agent --host webhook.site
    DENIED
      Reason: proxy_filtered

    $ nono why --profile py-agent --path ~/.ssh/id_ed25519 --op read
    DENIED
      Reason: filesystem_deny

.. container:: sd-fs-4 sd-text-left

    Denied something you need? **Edit the profile.**

.. Say: Then run nono profile validate py-agent. webhook.site is the AST01 catcher: denied by default.


Why nono is worth your time
===========================

.. container:: sd-fs-3 sd-text-left

    - **Works on real agents** — opencode ran unmodified.

    - **One tool, every axis** — network, writes, out-of-project reads.

    - **Zero changes to the skill** — the sandbox did all the work.


The one-line takeaway
=====================

.. container:: sd-fs-2 sd-text-center

    nono turns *'a skill could do anything'*

    into *'a skill does exactly what you granted.'*

.. container:: sd-fs-4 sd-text-center

    Give your agents skills. Then put them in a sandbox — **not optional**.

Questions?
==========

.. div:: sd-d-flex-row sd-align-major-center

    .. image:: images/fighting_agents.jpg
        :height: 460px
        :alt: Cleo wins the fight against the agents
        :align: center


Links — the standards
=====================

.. container:: sd-fs-4 sd-text-left

    **OWASP Top 10** (web apps) — https://owasp.org/www-project-top-ten/

    **OWASP Top 10 for LLM apps** — https://genai.owasp.org/llmrisk/

    **OWASP Agentic Skills Top 10** — https://github.com/OWASP/www-project-agentic-skills-top-10


Links — tools & further reading
===============================

.. container:: sd-fs-5 sd-text-left

    **opencode** — the coding agent — https://opencode.ai

    **nono** — the sandbox — https://docs.nono.sh · https://github.com/nolabs-ai/nono

    **webhook.site** — the capture server — https://webhook.site

    **The lethal trifecta** — Simon Willison — https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/

    **Sandboxing coding agents** — Anthropic — https://www.anthropic.com/engineering/claude-code-sandboxing

Notable resources/repos
=======================

    **Leaked system prompts** - https://github.com/asgeirtj/system_prompts_leaks

Built with
==========

.. container:: sd-fs-5 sd-text-left

    **reveal.js** via **sphinx-revealjs** — the slides — https://github.com/attakei/sphinx-revealjs

    **Sphinx** + **sphinx-design** — the build and the layout

    **jsphinx** + **Prism** — expandable, highlighted code snippets — https://github.com/barseghyanartur/jsphinx

    **marimo** — the ten live Part 1 notebooks — https://marimo.io

    **ttyd** — the embedded web terminal in the live demos — https://github.com/tsl0922/ttyd
