<h1>Blog API</h1>
<h3 align=center>First step</h3>
<b>Download project:</b>
<p><code>git clone https://github.com/bilitskyiA/testing-blog-api.git</code></p>
<h3 align=center>Second step</h3>
<b>Install Docker, Docker-Compose:</b>

<a>https://docs.docker.com/v17.09/engine/installation/</a>

<p>Create environments "conteiner.env", for example "example_conteiner.env"</p>

<h3 align=center>Third step</h3>

<b>Build and run docker images</b>
<p>From main folder "blog/"</p>
<p><code>docker-compose up --build</code></p>

<b>If you want to create superuser</b>
<p>In another terminal window from dir "blog/":</p>
<code>./m createsuperuser</code>
<p>Write username, email(if you don't need just press 'Enter'), password.</p>

<h3 align=center>Forth step</h3>

<b>Run Bot</b>
<p>From main folder "blog/"</p>
<p>Create python environments: <code>python3 -m venv venv</code></p>
<p>Activate python environments: <code>. venv/bin/activate</code></p>
<p>Install python requirements: <code>pip install -r requirements.txt</code></p>
Add configs to confgis.json file:
<code>

    {
      "max_users_num": integer, Max num of users that bot can create,
      "max_posts_num_per_user": integer, Max num of posts that each user can create,
      "max_votes_num_per_user": integer, Max num of votes that each user can create
    }
</code>

<p>Run bot:<code>python main.py</code></p>
