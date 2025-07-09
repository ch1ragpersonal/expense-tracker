import { useEffect, useState } from 'react';

function ExpenseList(){
    const [expenses, setExpenses] = useState([]);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchExpenses = async () => {
            const token = localStorage.getItem('access_token');

            try {
                const response = await fetch('http://localhost:8000/expenses', {
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
        fetchExpenses();
    }, []);

    return (
        <div className="bg-white p-6 rounded-xl shadow-md max-w-2xl w-full mt-8">
          <h2 className="text-xl font-bold mb-4">Your Expenses</h2>
    
          {error && <p className="text-red-500 mb-4">{error}</p>}
    
          {expenses.length === 0 ? (
            <p className="text-gray-500">No expenses yet.</p>
          ) : (
            <ul className="space-y-2">
              {expenses.map((expense) => (
                <li
                  key={expense.id}
                  className="border p-4 rounded-md flex justify-between"
                >
                  <div>
                    <p className="font-semibold">{expense.title}</p>
                    <p className="text-sm text-gray-500">{expense.category} • {new Date(expense.date).toLocaleDateString()}</p>
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