import { useEffect, useState } from 'react';

function ExpenseList(){
    const [expenses, setExpenses] = useState([]);
    const [category, setCategory] = useState('');
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [error, setError] = useState('');

    const fetchExpenses = async () => {
        const token = localStorage.getItem('access_token');

        const params = new URLSearchParams();
        if (category) {
            params.append('category', category);
        }
        if (startDate){
            params.append('startDate', startDate);
        } 
        if (endDate) params.append('endDate', endDate);

        const url = `http://localhost:8000/expenses/?${params.toString()}`;

        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });

            if (!response.ok){
                const err = await response.json();
                throw new Error(err.detail || 'Failed to fetch expenses');
            }

            const data = await response.json();
            setExpenses(data);
        } catch (err) {
            setError(err.message);
        }
    };
    useEffect(() => {
        fetchExpenses();
    }, []);

    return (
        <div className="bg-white p-6 rounded-xl shadow-md max-w-2xl w-full mt-8 space-y-4">
          <h2 className="text-xl font-bold">Your Expenses</h2>
    
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <input
              type="text"
              placeholder="Category"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="border p-2 rounded"
            />
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              className="border p-2 rounded"
            />
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              className="border p-2 rounded"
            />
            <button
            onClick={fetchExpenses}
            className="col-span-1 md:col-span-3 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
            Apply Filters
            </button>
          </div>
    
          {error && <p className="text-red-500">{error}</p>}
    
          {expenses.length === 0 ? (
            <p className="text-gray-500">No matching expenses.</p>
          ) : (
            <ul className="space-y-2">
              {expenses.map((expense) => (
                <li key={expense.id} className="border p-4 rounded flex justify-between">
                  <div>
                    <p className="font-semibold">{expense.title}</p>
                    <p className="text-sm text-gray-500">
                      {expense.category} • {new Date(expense.date).toLocaleDateString()}
                    </p>
                  </div>
                  <p className="font-bold">${expense.amount.toFixed(2)}</p>
                </li>
              ))}
            </ul>
          )}
        </div>
      );
}

export default ExpenseList;