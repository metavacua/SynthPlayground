import json

def main():
    raw_data = "This is the raw data."
    print(json.dumps({"raw_data": raw_data}))

if __name__ == "__main__":
    main()
