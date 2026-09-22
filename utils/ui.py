import pandas as pd

def style_playfair_grid(matrix_5x5, key_chars=None, highlight_coords=None):
    """
    Returns a pandas Styler object for the 5x5 Playfair matrix using standard pandas styling.
    No raw HTML/CSS injection.
    """
    df = pd.DataFrame(matrix_5x5, columns=[f"K{i+1}" for i in range(5)], index=[f"B{i+1}" for i in range(5)])
    
    if key_chars is None:
        key_chars = set()
    if highlight_coords is None:
        highlight_coords = {}

    def highlight_cells(data):
        styles = pd.DataFrame('', index=data.index, columns=data.columns)
        for r in range(5):
            for c in range(5):
                pos = (r, c)
                if pos in highlight_coords:
                    status = highlight_coords[pos]
                    if status == "active":
                        styles.iloc[r, c] = 'background-color: #fef08a; color: #854d0e; font-weight: bold;'
                    elif status == "result":
                        styles.iloc[r, c] = 'background-color: #bbf7d0; color: #166534; font-weight: bold;'
                elif data.iloc[r, c] in key_chars:
                    styles.iloc[r, c] = 'font-weight: bold; text-decoration: underline;'
        return styles

    return df.style.apply(highlight_cells, axis=None)

def format_aes_state_dataframe(state_4x4):
    """
    Converts a 4x4 AES state matrix of bytes into a clean pandas DataFrame with hex strings.
    """
    hex_matrix = []
    for r in range(4):
        row = [f"{val:02X}" if isinstance(val, int) else str(val) for val in state_4x4[r]]
        hex_matrix.append(row)
    return pd.DataFrame(hex_matrix, columns=["Col 0", "Col 1", "Col 2", "Col 3"], index=["Row 0", "Row 1", "Row 2", "Row 3"])
