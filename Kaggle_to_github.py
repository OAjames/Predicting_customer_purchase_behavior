# import os
# import subprocess
# import zipfile
# import glob

# # === CONFIGURATION ===
# kaggle_dataset = "psparks/instacart-market-basket-analysis"
# repo_path = r"C:\Users\AkanbiOlakunle\Documents\Instacart Market Basket Analysis\instacart-market-basket-analysis"  # ← CHANGE THIS to your local repo folder
# branch_name = "main"
# commit_message = "Added Instacart Market Basket Analysis dataset"

# # === STEP 1: DOWNLOAD DATASET FROM KAGGLE ===
# os.system(f"kaggle datasets download -d {kaggle_dataset} -p {repo_path}")

# # === STEP 2: UNZIP ANY DOWNLOADED ZIP FILES ===
# for zip_file in glob.glob(os.path.join(repo_path, "*.zip")):
#     print(f"Extracting {zip_file} ...")
#     with zipfile.ZipFile(zip_file, 'r') as zip_ref:
#         zip_ref.extractall(repo_path)
#     os.remove(zip_file)  # Cleanup zip files after extraction

# # === STEP 3: PUSH DATA TO GITHUB ===
# os.chdir(repo_path)
# subprocess.run(["git", "checkout", branch_name])
# subprocess.run(["git", "add", "."])
# subprocess.run(["git", "commit", "-m", commit_message])
# subprocess.run(["git", "push", "origin", branch_name])

# print("✅ Dataset successfully downloaded and pushed to GitHub!")


import os
import subprocess
import zipfile
import glob

# === CONFIGURATION ===
kaggle_dataset = "psparks/instacart-market-basket-analysis"
repo_path = r"C:\Users\AkanbiOlakunle\Documents\Instacart Market Basket Analysis\instacart-market-basket-analysis"
branch_name = "main"
commit_message = "Added Instacart Market Basket Analysis dataset"

# === STEP 1: DOWNLOAD DATASET FROM KAGGLE ===
try:
    subprocess.run(
        ["kaggle", "datasets", "download", "-d", kaggle_dataset, "-p", repo_path],
        check=True
    )
    print("✅ Dataset downloaded from Kaggle.")
except subprocess.CalledProcessError as e:
    print("❌ Error downloading dataset:", e)
    exit(1)

# === STEP 2: UNZIP ANY DOWNLOADED ZIP FILES ===
zip_files = glob.glob(os.path.join(repo_path, "*.zip"))
for zip_file in zip_files:
    print(f"📦 Extracting {zip_file} ...")
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(repo_path)
    os.remove(zip_file)
print("✅ Extraction complete.")

# === STEP 3: PUSH DATA TO GITHUB ===
os.chdir(repo_path)

try:
    subprocess.run(["git", "checkout", branch_name], check=True)
    subprocess.run(["git", "add", "."], check=True)

    # Check if there are staged changes
    result = subprocess.run(["git", "diff", "--cached", "--quiet"])
    if result.returncode != 0:
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push", "origin", branch_name], check=True)
        print("🚀 Changes committed and pushed to GitHub.")
    else:
        print("ℹ️ No changes to commit.")
except subprocess.CalledProcessError as e:
    print("❌ Git error:", e)
    exit(1)

print("✅ Dataset successfully downloaded and pushed to GitHub!")
