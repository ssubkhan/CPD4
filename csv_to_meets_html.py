import csv
import os
import re
import random

def csv_to_html(csv_filename, output_folder):
    html_filename = os.path.join(output_folder, os.path.splitext(os.path.basename(csv_filename))[0] + '.html')

    with open(csv_filename, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

        if len(rows) < 5:
            print("CSV file must have at least 5 rows.")
            return

        link_text = rows[0][0]
        h2_text = rows[1][0]
        link_url = rows[2][0]
        summary_text = rows[3][0]

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{link_text}</title>
    <link rel="stylesheet" href="../css/reset.css">
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <button class="mode-button" id="normal-mode" onclick="setMode('normal')">Normal</button>
    <button class="mode-button" id="dark-mode" onclick="setMode('dark')">Dark Mode</button>
    <button class="mode-button" id="high-contrast-mode" onclick="setMode('high-contrast')">High Contrast</button>
    
    <a href="#summary" class="skip-link">Skip to Main Content</a>
    <nav>
        <ul>
            <li><a href="../index.html">Home Page</a></li>
            <li><a href="#summary">Summary</a></li>
            <li><a href="#team-results">Team Results</a></li>
            <li><a href="#individual-results">Individual Results</a></li>
            <li><a href="#gallery">Gallery</a></li>
        </ul>
    </nav>

    

    <header>

     <div class="gif-container">
        <img src="../images/gif.gif" alt="Descriptive text for the GIF">
    </div>
    
        <h1><a href="{link_url}">{link_text}</a></h1>
        <h2>{h2_text}</h2>
    </header>
    <main id="main">
        <section class="summary" id="summary">
            <h2>Summary</h2>
            <p>{summary_text}</p>
        </section>

        <section id="team-results">
            <h2 class="sticky-header">Team Results (Place / Team / Score)</h2>
            <table>
        """

        table_start = True

        for row in rows[4:]:
            if len(row) == 3:
                if row[0] == "Place":
                    html_content += f"<tr><th>{row[0]}</th><th>{row[1]}</th><th>{row[2]}</th></tr>\n"
                else:
                    # Make the row focusable and readable by screen readers
                    html_content += f"""<tr tabindex="0" aria-label="Place: {row[0]}, Team: {row[1]}, Score: {row[2]}">
                                        <td>{row[0]}</td>
                                        <td>{row[1]}</td>
                                        <td>{row[2]}</td>
                                    </tr>\n"""

            elif len(row) == 8 and row[5].strip().lower() == 'ann arbor skyline':
                if table_start:
                    table_start = False
                    html_content += "</table>\n"


                    html_content += """</section>\n
                    <section id="individual-results">\n
                    
                     <h2 class="sticky-header">Individual Results</h2>
                     <div class="athlete-grid">"""  #  athlete-grid parent here

                place = row[0]
                grade = row[1]
                name = row[2]
                time = row[4]
                profile_pic = row[7]

                html_content += f"""
                <div class="athlete-card" tabindex="0">
                    <div class="card-inner">
                        <div class="card-front">
                            <figure> 
                            
                                <img src="../images/profiles/{profile_pic}" alt="Profile picture of {name}" 
                                 onerror="this.onerror=null; this.src='../images/default_image.jpg';"> 
                               <div class="name">{name}</div>  <!-- Display Name -->
                            </figure>
                        </div>
                        <div class="card-back">
                            <dl>
                                <dt>Place</dt><dd>{place}</dd>
                                <dt>Time</dt><dd>{time}</dd>
                                <dt>Grade</dt><dd>{grade}</dd>
                            </dl>
                        </div>
                    </div>
                </div>
                """

        html_content += """</div> <!-- Close athlete-grid -->
        </section>\n
        <section id="gallery">
              <h2 class="sticky-header">Gallery</h2>
            <div class="gallery-container">""" + create_meet_image_gallery(link_url) + """</div>
        </section>
        </main>   
        <footer>
            <p>
                Skyline High School<br>
                <address>
                2552 North Maple Road<br>
                Ann Arbor, MI 48103<br><br>
                <a href="https://sites.google.com/aaps.k12.mi.us/skylinecrosscountry2021/home">XC Skyline Page</a><br>
                Follow us on Instagram <a href="https://www.instagram.com/a2skylinexc/" aria-label="Instagram"><i class="fa-brands fa-instagram"></i></a>
            </p>
        </footer>
       
       <script src="../js/script.js"></script>
        </body>
        </html>
        """

        # Save HTML content to a file in the meets folder
        with open(html_filename, 'w', encoding='utf-8') as htmlfile:
            htmlfile.write(html_content)

        print(f"HTML file '{html_filename}' created successfully.")

def create_meet_image_gallery(url):
    try:
        meet_id = extract_meet_id(url)
    except ValueError as e:
        print(e)
        return ""
    
    folder_path = f'images/meets/{meet_id}/'

    if not os.path.exists(folder_path) or not os.listdir(folder_path):
        print(f"No images found in folder: {folder_path}")
        return ""
    
    selected_photos = select_random_photos(folder_path)
    html_image_tags = generate_image_tags(selected_photos, folder_path)
    
    return html_image_tags

def extract_meet_id(url):
    match = re.search(r"/meet/(\d+)", url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Meet ID not found in URL.")

def select_random_photos(folder_path, num_photos=12):
    all_files = os.listdir(folder_path)
    image_files = [f for f in all_files if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    
    if len(image_files) < num_photos:
        return image_files  # Return all if not enough
    
    return random.sample(image_files, num_photos)

def generate_image_tags(image_files, folder_path):
    img_tags = []
    
    for index, img in enumerate(image_files):
        img_path = os.path.join(folder_path, img)
        alt_text = f"Athlete running track course {index + 1}"  # Numbered alternative text
        img_tags.append(f'<img src="../{img_path}" alt="{alt_text}" />')
    
    return "\n".join(img_tags)


def process_meet_files():
    meets_folder = os.path.join(os.getcwd(), "meets")
    csv_files = [f for f in os.listdir(meets_folder) if f.endswith('.csv')]
    
    if not csv_files:
        print(f"No CSV files found in folder: {meets_folder}")
        return

    for csv_file in csv_files:
        csv_file_path = os.path.join(meets_folder, csv_file)
        csv_to_html(csv_file_path, meets_folder)

if __name__ == "__main__":
    process_meet_files()
