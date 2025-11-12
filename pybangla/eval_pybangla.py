import os
import pandas as pd
import jiwer
from tqdm import tqdm
import time
import csv
import difflib
from datetime import datetime
import numpy as np

from module.main import Normalizer

nrml = Normalizer()


def read_excel_file(file_path):
    """Read Excel file and return DataFrame"""
    df = pd.read_excel(file_path)
    return df


def get_detailed_diff(text1, text2):
    """Get detailed character-level differences between two texts"""
    differ = difflib.SequenceMatcher(None, text1, text2)
    diff_details = []
    
    for tag, i1, i2, j1, j2 in differ.get_opcodes():
        if tag != 'equal':
            diff_details.append({
                'operation': tag,
                'reviewed': text1[i1:i2],
                'normalized': text2[j1:j2],
                'position': f'{i1}-{i2}'
            })
    
    return diff_details


def evaluate_normalization(data, output_path):
    """Evaluate normalization and generate comprehensive report"""
    
    print("Evaluating normalization...")
    
    # Initialize results list
    results = []
    
    # Get input and reviewed texts
    input_texts = data['Input_Text'].tolist()
    reviewed_texts = data['Human_Review'].tolist()
    categories = data["category"].tolist()

    # input_texts = ["তার পাসপোর্ট নম্বর P87654321 ছিল।, 1995-1969 and phone number 01773-550379"]
    # reviewed_texts = ["তার পাসপোর্ট নম্বর পি, এইট, সেভেন, সিক্স, ফাইভ, ফোর, থ্রি, টু, ওয়ান, ছিল।, ওয়ান থাউজ্যান্ড নাইন হান্ড্রেড নাইনটি-ফাইভ - ওয়ান থাউজ্যান্ড নাইন হান্ড্রেড সিক্সটি-নাইন and phone number জিরো ওয়ান ডাবল সেভেন থ্রি ডাবল ফাইভ জিরো থ্রি সেভেন নাইন"]

    # Progress bar for evaluation
    for idx, (input_text, reviewed_text, category) in enumerate(tqdm(zip(input_texts, reviewed_texts, categories), 
                                                          total=len(input_texts), 
                                                          desc="Processing")):
        # Normalize text
        start_time = time.time()
        normalized_text = nrml.text_normalizer(input_text, all_operation=True)

        print("Input Text: ", input_text)
        print("Reviewed Text: ", reviewed_text)
        print("Normalized Text: ", normalized_text)
        processing_time = time.time() - start_time
        
        # Calculate metrics
        cer_score = jiwer.cer(str(reviewed_text), normalized_text)
        wer_score = jiwer.wer(str(reviewed_text), normalized_text)
        exact_match = str(reviewed_text) == normalized_text
        
        # Get character and word counts
        char_count_input = len(str(input_text))
        char_count_reviewed = len(str(reviewed_text))
        char_count_normalized = len(normalized_text)
        word_count_input = len(str(input_text).split())
        word_count_reviewed = len(str(reviewed_text).split())
        word_count_normalized = len(normalized_text.split())
        
        # Get differences if not exact match
        differences = ""
        if not exact_match:
            diff_details = get_detailed_diff(str(reviewed_text), normalized_text)
            differences = "; ".join([f"{d['operation']}: '{d['reviewed']}' → '{d['normalized']}' at {d['position']}" 
                                   for d in diff_details[:3]])  # Show first 3 differences
            if len(diff_details) > 3:
                differences += f" ... and {len(diff_details) - 3} more differences"
        
        # Compile result
        result = {
            'Index': idx + 1,
            'Input_Text': input_text,
            'Human_Review': reviewed_text,
            'Normalized_Text': normalized_text,
            'Exact_Match': exact_match,
            'CER': round(cer_score, 4),
            'WER': round(wer_score, 4),
            'Char_Count_Input': char_count_input,
            'Char_Count_Reviewed': char_count_reviewed,
            'Char_Count_Normalized': char_count_normalized,
            'Word_Count_Input': word_count_input,
            'Word_Count_Reviewed': word_count_reviewed,
            'Word_Count_Normalized': word_count_normalized,
            'Processing_Time_ms': round(processing_time * 1000, 2),
            'Category': category,
            'Differences': differences
        }
        
        results.append(result)
    
    # Create DataFrame from results
    results_df = pd.DataFrame(results)
    
    # Calculate summary statistics
    summary_stats = {
        'Total_Samples': len(results_df),
        'Exact_Matches': results_df['Exact_Match'].sum(),
        'Exact_Match_Rate': f"{(results_df['Exact_Match'].sum() / len(results_df) * 100):.2f}%",
        'Average_CER': round(results_df['CER'].mean(), 4),
        'Median_CER': round(results_df['CER'].median(), 4),
        'Min_CER': round(results_df['CER'].min(), 4),
        'Max_CER': round(results_df['CER'].max(), 4),
        'Average_WER': round(results_df['WER'].mean(), 4),
        'Average_Processing_Time_ms': round(results_df['Processing_Time_ms'].mean(), 2),
        'CER_Less_Than_0.05': (results_df['CER'] < 0.05).sum(),
        'CER_Less_Than_0.10': (results_df['CER'] < 0.10).sum(),
    }

    # catergory-wise summary performance report
    category_summary = results_df.groupby('Category').agg(
        Total_Samples=('Index', 'count'),
        Exact_Matches=('Exact_Match', 'sum'),
        Average_CER=('CER', 'mean'),
        Average_WER=('WER', 'mean'),
        Average_Processing_Time_ms=('Processing_Time_ms', 'mean')
    ).reset_index()
    
    # Create summary DataFrame
    summary_df = pd.DataFrame([summary_stats])
    
    # Create error analysis
    error_df = results_df[results_df['Exact_Match'] == False].copy()
    error_df = error_df[['Index', 'Input_Text', 'Human_Review', 'Normalized_Text', 'CER', 'Differences']]
    
    # Save to Excel with multiple sheets
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Write main results
        results_df.to_excel(writer, sheet_name='Evaluation_Results', index=False)
        
        # Write summary statistics
        summary_df.to_excel(writer, sheet_name='Summary_Statistics', index=False)
        category_summary.to_excel(writer, sheet_name='Category_Summary', index=False)

        # Write error analysis
        if not error_df.empty:
            error_df.to_excel(writer, sheet_name='Error_Analysis', index=False)
        
        # Format the Excel file
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            
            # Adjust column widths
            for column in worksheet.columns:
                max_length = 0
                column = [cell for cell in column]
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
    
    # Print summary to console
    print("\n" + "="*60)
    print("EVALUATION SUMMARY")
    print("="*60)
    print(f"Total Samples: {summary_stats['Total_Samples']}")
    print(f"Exact Matches: {summary_stats['Exact_Matches']} ({summary_stats['Exact_Match_Rate']})")
    print(f"Average CER: {summary_stats['Average_CER']}")
    print(f"Average WER: {summary_stats['Average_WER']}")
    print(f"Average Processing Time: {summary_stats['Average_Processing_Time_ms']} ms")
    print(f"Samples with CER < 0.05: {summary_stats['CER_Less_Than_0.05']}")
    print(f"Samples with CER < 0.10: {summary_stats['CER_Less_Than_0.10']}")
    print("="*60)
    
    # Save a detailed CSV report as well
    csv_path = output_path.replace('.xlsx', '_detailed.csv')
    results_df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    
    print(f"\nReports saved to:")
    print(f"  - Excel: {output_path}")
    print(f"  - CSV: {csv_path}")
    
    return results_df, summary_stats


def generate_comparison_report(results_df, output_path):
    """Generate a side-by-side comparison report for manual review"""
    
    comparison_path = output_path.replace('.xlsx', '_comparison.txt')
    
    with open(comparison_path, 'w', encoding='utf-8') as f:
        f.write("NORMALIZATION COMPARISON REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*80 + "\n\n")
        
        for _, row in results_df.iterrows():
            if not row['Exact_Match']:
                f.write(f"Sample #{row['Index']}\n")
                f.write("-"*80 + "\n")
                f.write(f"Input:      {row['Input_Text']}\n")
                f.write(f"Expected:   {row['Human_Review']}\n")
                f.write(f"Normalized: {row['Normalized_Text']}\n")
                f.write(f"CER: {row['CER']:.4f} | WER: {row['WER']:.4f}\n")
                f.write(f"Differences: {row['Differences']}\n")
                f.write("\n")
    
    print(f"  - Comparison: {comparison_path}")


if __name__ == "__main__":
    # Configuration
    input_eval_data_path = "./eval_data/eval_data.xlsx"
    output_eval_data_path = "./report/eval_data_2.15.0.xlsx"
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_eval_data_path), exist_ok=True)
    
    # Read data
    print(f"Reading evaluation data from: {input_eval_data_path}")
    data = read_excel_file(input_eval_data_path)
    print(f"Loaded {len(data)} samples for evaluation\n")
    
    # Run evaluation
    results_df, summary_stats = evaluate_normalization(data, output_eval_data_path)
    
    # Generate additional comparison report
    generate_comparison_report(results_df, output_eval_data_path)
    
    print("\nEvaluation completed successfully!")