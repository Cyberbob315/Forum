/*
Please consider that the JS part isn't production ready at all, I just code it to show the concept of merging filters and titles together !
*/
const TAB_KEY = '9';
$(document).ready(function () {
    $('.filterable .btn-filter').click(function () {
        let $panel = $(this).parents('.filterable'),
            $filters = $panel.find('.filters input'),
            $tbody = $panel.find('.table tbody');
        if ($filters.prop('disabled') === true) {
            $filters.prop('disabled', false);
            $filters.first().focus();
        } else {
            $filters.val('').prop('disabled', true);
            $tbody.find('.no-result').remove();
            $tbody.find('tr').show();
        }
    });

    function isComparator(char) {
        return char === '>' || char === '<';
    }

    $('.mark-filter').keyup(function (e) {
        let code = e.keyCode || e.which;
        if (code === TAB_KEY) return;
        let input = $(this);
        let inputContent = input.val().toLowerCase();
        let panel = input.parents('.filterable');
        let column = panel.find('.filters th').index(input.parents('th'));
        let table = panel.find('.table');
        let rows = table.find('tbody tr');
        let filteredRows = rows.filter(function () {
            let rowValue = $(this).find('td').eq(column).text().toLowerCase();
            if (inputContent.length === 1 && isComparator(inputContent[0])) return false;
            let inputValue;
            let isEqual = inputContent[1] === '=';
            if (isEqual && inputContent.length === 2) return false;
            if (isComparator(inputContent[0])) {
                if (isEqual)
                    inputValue = inputContent.substring(2);
                else
                    inputValue = inputContent.substring(1);
                if (isNaN(inputValue))
                    return rowValue.indexOf(inputContent) === -1;
                let inputFloat = parseFloat(inputValue);
                let valueFloat = parseFloat(rowValue);
                if (!isEqual && inputFloat === valueFloat) return true;
                switch (inputContent[0]) {
                    case '>':
                        return inputValue > valueFloat;
                    case '<':
                        return inputValue < valueFloat;
                }
            } else {
                return rowValue.indexOf(inputContent) === -1;
            }
        });
        table.find('tbody .no-result').remove();
        rows.show();
        filteredRows.hide();
        if (filteredRows.length === rows.length) {
            table.find('tbody').prepend($('<tr class="no-result text-center"><td colspan="'
                + table.find('.filters th').length + '">No result found</td></tr>'));
        }

    });

    $('.normal-filter').keyup(function (e) {
        /* Ignore tab key */
        let code = e.keyCode || e.which;
        if (code === TAB_KEY) return;
        /* Useful DOM data and selectors */
        let $input = $(this),
            inputContent = $input.val().toLowerCase(),
            $panel = $input.parents('.filterable'),
            column = $panel.find('.filters th').index($input.parents('th')),
            $table = $panel.find('.table'),
            $rows = $table.find('tbody tr');
        /* Dirtiest filter function ever ;) */
        let $filteredRows = $rows.filter(function () {
            let value = $(this).find('td').eq(column).text().toLowerCase();
            return value.indexOf(inputContent) === -1;
        });
        /* Clean previous no-result if exist */
        $table.find('tbody .no-result').remove();
        /* Show all rows, hide filtered ones (never do that outside of a demo ! xD) */
        $rows.show();
        $filteredRows.hide();
        /* Prepend no-result row if all rows are filtered */
        if ($filteredRows.length === $rows.length) {
            $table.find('tbody').prepend($('<tr class="no-result text-center"><td colspan="' + $table.find('.filters th').length + '">No result found</td></tr>'));
        }
    });
});
