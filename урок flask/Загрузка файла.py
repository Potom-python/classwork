from flask import Flask, request, url_for

app = Flask(__name__)


@app.route("/load_photo", methods=['POST', 'GET'])
def load_photo():
    if request.method == 'GET':
        return f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="{url_for('static', filename='css/style_load_photo.css')}">
    <title>Отбор астронавтов</title>
  </head>
  <body>
    <h1>Загрузка фотографии</h1>
    <h2>для участия в миссии</h2>
    <div>
      <form class="login_form" method="post" enctype="multipart/form-data">
        <div class="form-group">
          <input type="file" id="photoInput" name="photo" accept="image/*" class="form-control">
          <img id="imagePreview" src="#" alt="Ваше фото" style="max-width: 600px; display: none; margin-top: 10px;">
        </div>
        <button type="submit" class="btn btn-primary">Отправить</button>
      </form>
    </div>

    <script>
      document.getElementById('photoInput').addEventListener('change', function(event) {{
        const file = event.target.files[0];
        if (file) {{
          const reader = new FileReader();
          reader.onload = function(e) {{
            const preview = document.getElementById('imagePreview');
            preview.src = e.target.result;
            preview.style.display = 'block';
          }}
          reader.readAsDataURL(file);
        }}
      }});

      // document.getElementById('photoInput').addEventListener('change', function() {{
      //   this.form.submit();
      // }});
    </script>
  </body>
</html>'''


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
