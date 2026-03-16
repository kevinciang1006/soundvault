/**
 * Converts short-form key to long-form display format
 * @param shortKey - Key in format "C" or "Gm"
 * @returns Key in format "C Major" or "G Minor"
 * @example
 * convertToLongFormat("C") // "C Major"
 * convertToLongFormat("Gm") // "G Minor"
 */
export function convertToLongFormat(shortKey: string): string {
  if (shortKey.endsWith('m')) {
    // Minor key: "Gm" → "G Minor"
    return `${shortKey.slice(0, -1)} Minor`
  } else {
    // Major key: "C" → "C Major"
    return `${shortKey} Major`
  }
}

/**
 * Checks if a key is minor
 * @param key - Key in short format ("Gm") or long format ("G Minor")
 * @returns true if minor, false if major
 */
export function isMinorKey(key: string): boolean {
  return key.endsWith('m') || key.includes('Minor')
}

/**
 * Extracts the root note from a key
 * @param key - Key in short or long format
 * @returns Root note (e.g., "C", "G#", "F")
 */
export function getRootNote(key: string): string {
  return key.replace('m', '').replace(' Minor', '').replace(' Major', '').trim()
}
