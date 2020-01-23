use std::env;
use std::fs::File;
use std::path::PathBuf;
use std::io::Read;
use http::{header, request, response};

fn load_payload(payload: &PathBuf) -> std::io::Result<Vec<u8>> {
    let mut file = File::open(&payload)?;

    let mut buffer: Vec<u8> = Vec::with_capacity(file.metadata().unwrap().len() as usize);

    file.read_to_end(&mut buffer)?;
    Ok(buffer)
}

fn encode_payload(filename: &str, payload_buffer: &Vec<u8>) -> zip::result::ZipResult<Vec<u8>> {
    use std::io::Write;

    let buf: &mut [u8] = &mut [0u8; 1024];
    let w = std::io::Cursor::new(buf);
    let mut zip = zip::ZipWriter::new(w);

    let options = zip::write::FileOptions::default().compression_method(zip::CompressionMethod::Deflated);
    zip.start_file(filename, options)?;
    zip.write(payload_buffer)?;

    // Optionally finish the zip. (this is also done on drop)
    Ok(zip.finish().unwrap().into_inner().to_vec())
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

            println!("Zipped file: {:?}", encode_payload(&args[1], &buffer).unwrap());
        }
        _ => {
            print_help();
        }
    }
}
