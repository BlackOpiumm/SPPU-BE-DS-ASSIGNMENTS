#include<stdio.h>
#include<stdlib.h>
#include<omp.h>
#include<time.h>

int main()
{
    int N, threads;

    printf("Enter array size: ");
    scanf("%d", &N);

    printf("Enter number of threads: ");
    scanf("%d", &threads);

    int arr[N];
    int partial[threads];

    srand(time(0));

    // Generate random array
    for(int i=0; i<N; i++)
    {
        arr[i] = rand() % 100;
    }

    // Display full array
    printf("\nFull Array:\n");

    for(int i=0; i<N; i++)
    {
        printf("%d ", arr[i]);
    }

    // ---------------- SEQUENTIAL ----------------

    double start_seq = omp_get_wtime();

    int seq_sum = 0;

    for(int i=0; i<N; i++)
    {
        seq_sum += arr[i];
    }

    double end_seq = omp_get_wtime();

    // Initialize partial sums
    for(int i=0; i<threads; i++)
    {
        partial[i] = 0;
    }

    // ---------------- PARALLEL ----------------

    double start_par = omp_get_wtime();

    #pragma omp parallel num_threads(threads)
    {
        int tid = omp_get_thread_num();

        for(int i=tid; i<N; i+=threads)
        {
            partial[tid] += arr[i];
        }
    }

    double end_par = omp_get_wtime();

    int total = 0;

    // Thread-wise data
    printf("\n\nThread Wise Data:\n");

    for(int t=0; t<threads; t++)
    {
        printf("\nThread %d elements: ", t);

        for(int i=t; i<N; i+=threads)
        {
            printf("%d ", arr[i]);
        }

        printf("\nPartial Sum = %d\n", partial[t]);

        total += partial[t];
    }

    // ---------------- RESULTS ----------------

    printf("\nSequential Sum = %d\n", seq_sum);

    printf("Parallel Sum = %d\n", total);

    printf("\nSequential Time = %f sec\n",
           end_seq - start_seq);

    printf("Parallel Time = %f sec\n",
           end_par - start_par);

    return 0;
}